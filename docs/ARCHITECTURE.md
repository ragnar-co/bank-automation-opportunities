# Automation Opportunity Finder — ARCHITECTURE

Project: `Automation Opportunity Finder`  
Document ID: `architecture`  
Template: `ddd-web-app-v2.8.0`  
Status: Draft for implementation  
Depends on: `prd`, `constraints`, `scope`, `personas`

## System Diagram

```text
bank_automation_opportunities.csv
              |
              v
      Import / Seed Command
              |
      Schema + Row Validation
              |
              v
           SQLite3 (tasks)
              |
       Query / App Layer
       /       |        \
      v        v         v
 Task Effort  Dept Sum   Top 3
       \       |        /
              v
      Browser (Flask / Jinja)
       +-- Dashboard            GET  /
       +-- Task Detail          GET  /tasks/<task_id>
       +-- Saved Explorations   GET  /explorations
              |
       Disclaimer visible on every surface showing Weekly Effort

Bonus path:
Task Detail "Generate AI Exploration" -> POST /tasks/<task_id>/explorations
              |
              v
       ai_service.py (adapter; sole provider boundary)
              |
              v
       Company AI endpoint
              |
              v
     structured exploration result
     (recommendation, rationale, verification_points)
              |
              v
     SQLite3 (exploration_recommendations, FK -> tasks.task_id)
              |
              +--> displayed on Task Detail
              +--> displayed on Saved Explorations

AI failure/unavailability renders an error state on Task Detail only;
Dashboard, Task Detail's own task data, department totals, and Top 3 are
unaffected (AI adapter is isolated from the core query layer).
```

## Tech Stack Decisions

- Database: SQLite3.
  - เหตุผล: dataset ขนาดเล็กพอ, setup/deploy ง่าย, รองรับทั้ง raw tasks และ persisted AI recommendations ใน store เดียว.
  - Why not DuckDB: DuckDB เหมาะกับ analytical scan มาก แต่โจทย์นี้ต้องการ web app ขนาดเล็กและ bonus มี write-back; SQLite3 ลด moving parts ภายใต้เวลา 120 นาที.
- CSV ingestion: command/script ที่รันก่อนเปิดใช้งาน core UI.
  - Why not browser upload: ไม่ใช่ requirement explicit และเพิ่ม multipart/error UX โดยไม่เพิ่ม core scoring signal.
- Weekly Effort: คำนวณ query-time ด้วย `weekly_runs * minutes_per_run`.
  - Why not persist derived value: ลดโอกาส derived column stale ถ้า source values เปลี่ยน.
- Web framework/runtime: **Python 3 / Flask 3.0.3**, server-rendered Jinja templates, vanilla JavaScript/CSS (no SPA framework), served in production by **Gunicorn 22.0.0**.
  - Why: repo was empty at start, no existing frontend framework, and the requirement is a simple dashboard — not a complex SPA. Server-rendered pages (POST → redirect → GET) keep implementation risk low.
  - Why not a JS framework/SPA: no client-side state worth a framework; the AI-exploration flow is a single form submit, not an interactive app.
- AI provider/model: **OpenRouter** (`https://openrouter.ai/api/v1/chat/completions`), model `anthropic/claude-sonnet-4.6`, as a time-boxed stand-in for the company's own AI endpoint — see `docs/ADR.md` ADR-005 for why, and for how the model/provider choice was verified (not guessed) against this account's restrictions. The call is isolated behind `app/ai_service.py` so the provider can be swapped (e.g. to the company's permanent endpoint) without touching `app/routes.py` or the core query layer. The API key (`AI_API_KEY`) expires ~24h after issuance and must be rotated or replaced before relying on this in a durable deployment; it is read only from the environment, never committed to the repository.

## Deployment Architecture

```text
Company Git Repo
      |
      v
   Coolify
      |
      v
Web Application Container
      |
      +---- SQLite database file / persistent volume
      |
      +---- Environment secrets
             \-- AI endpoint token (bonus only)
```

- Production URL ต้องเปิด core analytics ได้หลัง deploy.
- SQLite database ต้องอยู่ใน persistent storage หาก deployment restart แล้วข้อมูลต้องคงอยู่.
- Build: `docker build` from the repo `Dockerfile` (python:3.12-slim base). Start: container entrypoint runs the idempotent CSV import (only if `DATABASE_PATH` does not yet exist) then starts `gunicorn --bind 0.0.0.0:$PORT app:app`.
- `docker-compose.yaml` ไม่ publish host port ตรงๆ (ใช้ `expose` แทน `ports`) เพราะ Coolify เป็น shared host ที่มีหลาย app/บริการใช้ port ของ host อยู่แล้ว (ชนกับ dashboard ของ Coolify เองตอนลองจริง) — Traefik ของ Coolify เข้าถึง container ผ่าน internal network แทน ดูเหตุผลเต็มที่ `docs/ADR.md` ADR-006. การรัน local ใช้ `docker-compose.override.yml` (ไม่ถูก Coolify อ่าน) เพื่อ publish `localhost:8000` สำหรับ dev เท่านั้น.

## Scalability Strategy

- Current dataset: 12,419 rows จากไฟล์ตัวอย่าง; architecture นี้ optimize เพื่อความเรียบง่ายและความน่าเชื่อถือในข้อสอบ ไม่ใช่ high-scale multi-tenant platform.
- Index ที่ควรพิจารณาเมื่อ implement: `task_id` unique/primary key; index บน `department` หาก query plan/latency ที่วัดจริงแสดงว่าจำเป็น.
- Scaling threshold: `null` — calibration owner: Developer; ต้องอิง measurements ไม่เดาตัวเลข.
- ถ้าข้อมูลโตจน SQLite ไม่เหมาะ ให้มี migration path ไป relational/analytical store ภายหลัง โดยไม่เปลี่ยน semantic ของ Weekly Effort.

## Third-party Integrations

| Integration | Purpose | Core/Bonus | Failure behavior |
|---|---|---|---|
| Company Git repository | source submission | Core | ไม่มีผล runtime แต่เป็น submission blocker |
| Coolify | production deployment | Core | ถ้า deploy ไม่ผ่านถือว่า core ยังไม่ส่งมอบ |
| AI endpoint (currently OpenRouter, time-boxed company key — see ADR-005) | สร้าง exploration recommendation | Bonus | ต้อง fail independently; core dashboard ยังใช้ได้ |
| Claude Code/Codex | coding workflow | Build-time | ไม่ใช่ runtime dependency |
| Google Fonts CDN (`fonts.googleapis.com`/`fonts.gstatic.com`) | โหลด webfonts (Fraunces, IBM Plex Sans Thai, IBM Plex Mono) สำหรับ UI | Core (visual only) | Client-side only; ถ้าบล็อกหรือโหลดไม่ได้ browser จะ fallback ไปใช้ font ที่ประกาศไว้ในฝั่ง fallback ของ CSS (`serif`/`sans-serif`/`monospace`) — หน้าเว็บยังอ่านและใช้งานได้ปกติ ไม่กระทบ core analytics |

## Observability & SLOs

- SLO availability: `null` — calibration owner: Developer; วัดจาก deployed app ก่อนกำหนด.
- SLO latency: `null` — calibration owner: Developer; วัดหน้า summary/query จริงก่อนกำหนด.
- Structured logging: import result, validation failure, application error และ AI call failure (bonus) ควรมี log ที่ระบุ operation และ error โดยไม่ log secret.
- Import reconciliation: บันทึกจำนวน rows read / accepted / rejected ใน run output เพื่อใช้ตรวจสอบ ingestion.
- Core health signal: `GET /health` — currently a static liveness check (process is up); does not yet verify SQLite accessibility. Readiness (DB reachable) vs. liveness (process up) should be made explicit before relying on this for deploy gating — calibration owner: Developer.
- Alert thresholds และ incident severity ยังไม่ประกาศที่นี่; เป็นหน้าที่ RUNBOOK.md ในชุดเต็ม.

Validation Checklist
- [x] ครบ 6 suggested headings ของ ARCHITECTURE.md
- [x] architecture trace กลับ PRD/SCOPE/CONSTRAINTS ได้
- [x] มีเหตุผลและ why-not สำหรับการตัดสินใจหลัก
- [x] ไม่มี SLO/threshold ที่เดาขึ้นมา
- [x] AI bonus ล้มเหลวได้โดยไม่ทำให้ core analytics ล้มตาม
- [x] Weekly Effort ยังคง semantic ว่า current effort ไม่ใช่ savings
