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
           SQLite3
              |
       Query / App Layer
       /       |        \
      v        v         v
 Task Effort  Dept Sum   Top 3
       \       |        /
              v
            Web UI
              |
       Disclaimer visible

Bonus path:
SQLite3 aggregates -> Company AI endpoint -> structured exploration proposal
                                      |-> persist in SQLite3 -> display in Web UI
```

## Tech Stack Decisions

- Database: SQLite3.
  - เหตุผล: dataset ขนาดเล็กพอ, setup/deploy ง่าย, รองรับทั้ง raw tasks และ persisted AI recommendations ใน store เดียว.
  - Why not DuckDB: DuckDB เหมาะกับ analytical scan มาก แต่โจทย์นี้ต้องการ web app ขนาดเล็กและ bonus มี write-back; SQLite3 ลด moving parts ภายใต้เวลา 120 นาที.
- CSV ingestion: command/script ที่รันก่อนเปิดใช้งาน core UI.
  - Why not browser upload: ไม่ใช่ requirement explicit และเพิ่ม multipart/error UX โดยไม่เพิ่ม core scoring signal.
- Weekly Effort: คำนวณ query-time ด้วย `weekly_runs * minutes_per_run`.
  - Why not persist derived value: ลดโอกาส derived column stale ถ้า source values เปลี่ยน.
- Web framework/runtime: `null` — calibration owner: Developer; เลือก framework ที่มี scaffold/deploy path พร้อมที่สุดใน environment สอบ แล้วอัปเดตเอกสารนี้ก่อนถือเป็น final.
- AI provider/model: company-provided endpoint; model identifier/quota = `null` — calibration owner: Platform owner/Developer.

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
- วิธี build/start ที่แน่นอนขึ้นกับ framework ที่เลือกและต้องบันทึกก่อน final deploy.

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
| Company AI endpoint | สร้าง exploration recommendation | Bonus | ต้อง fail independently; core dashboard ยังใช้ได้ |
| Claude Code/Codex | coding workflow | Build-time | ไม่ใช่ runtime dependency |

## Observability & SLOs

- SLO availability: `null` — calibration owner: Developer; วัดจาก deployed app ก่อนกำหนด.
- SLO latency: `null` — calibration owner: Developer; วัดหน้า summary/query จริงก่อนกำหนด.
- Structured logging: import result, validation failure, application error และ AI call failure (bonus) ควรมี log ที่ระบุ operation และ error โดยไม่ log secret.
- Import reconciliation: บันทึกจำนวน rows read / accepted / rejected ใน run output เพื่อใช้ตรวจสอบ ingestion.
- Core health signal: application process + DB access; concrete health endpoint = `null` — calibration owner: Developer หลังเลือก framework.
- Alert thresholds และ incident severity ยังไม่ประกาศที่นี่; เป็นหน้าที่ RUNBOOK.md ในชุดเต็ม.

Validation Checklist
- [x] ครบ 6 suggested headings ของ ARCHITECTURE.md
- [x] architecture trace กลับ PRD/SCOPE/CONSTRAINTS ได้
- [x] มีเหตุผลและ why-not สำหรับการตัดสินใจหลัก
- [x] ไม่มี SLO/threshold ที่เดาขึ้นมา
- [x] AI bonus ล้มเหลวได้โดยไม่ทำให้ core analytics ล้มตาม
- [x] Weekly Effort ยังคง semantic ว่า current effort ไม่ใช่ savings
