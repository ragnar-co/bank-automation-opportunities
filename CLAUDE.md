# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

This repository contains a working core MVP, plus the AI-exploration bonus path currently
being built out. Stack is implemented (not `null`) — see below.

**Stack:**
- Python 3 / Flask 3.0.3
- SQLite3 (stdlib `sqlite3`)
- Jinja server-rendered templates + vanilla JS/CSS (no frontend framework, no SPA)
- pytest
- Gunicorn (production WSGI server)
- Docker, deployed to Coolify

**Directory structure:**
```
app/                  Flask application package
  __init__.py           creates the Flask instance (template_folder/static_folder point at
                         the project-root templates/ and static/, not app/templates)
  routes.py             all route handlers
  db.py                 SQLite3 access layer
  ai_service.py         AI provider adapter (sole boundary — see ADR-004/ADR-005)
run.py                Dev entrypoint: python run.py (Flask debug server)
templates/, static/  Jinja templates + CSS/JS, at project root (not inside app/)
scripts/import_csv.py CSV import/seed command
tests/                pytest suite
docs/                 DDD documents (PRD, ARCHITECTURE, ADR, DATA_MODEL, UI_SPEC, ...)
data/                 SQLite file lives here by default (gitignored; DATABASE_PATH overrides)
Dockerfile, docker-compose.yaml   container build + local multi-container run
```

**Commands:**
```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/import_csv.py          # seed SQLite from the CSV (run once against a fresh/empty DB; re-running against an already-seeded DB will fail on duplicate task_id)
.venv/bin/python -m pytest                      # run tests
.venv/bin/python run.py                         # dev server (Flask debug)
.venv/bin/gunicorn --bind 0.0.0.0:8000 app:app  # production-style run (app: package, app: Flask instance)
cp .env.example .env && docker compose up --build  # local Docker test (mirrors Coolify's docker-compose-based deploy)
```

## What this project is

"Automation Opportunity Finder" — a web app that ingests the CSV of recurring task data,
validates and persists it to SQLite3, shows which tasks/departments consume the most
recurring weekly time, and (bonus) lets a user request an AI-generated exploration
recommendation per task so management can prioritize what to explore for automation next.

Read these in order before implementing anything; each has a `Depends on` field at the top:
`docs/CONSTRAINTS.md` → `docs/PERSONAS.md` / `docs/VPD.md` → `docs/SCOPE.md` → `docs/PRD.md`
→ `docs/ARCHITECTURE.md` → `docs/ADR.md` → `docs/DATA_MODEL.md` → `docs/UI_SPEC.md` →
`docs/GLOSSARY.md`. `docs/DATA_MODEL.md` is the canonical owner of entity/schema names;
`docs/ARCHITECTURE.md` is the canonical owner of the tech stack.

## Core data model

Canonical schema: `docs/DATA_MODEL.md`. Summary:

- `tasks` — one row per validated task imported from `bank_automation_opportunities.csv`
  (~12,419 rows, 8 departments): `task_id` (PK), `department`, `task_name`, `weekly_runs`,
  `minutes_per_run`.
  - **Weekly Effort** (`weekly_minutes`) = `weekly_runs * minutes_per_run`, computed at query
    time in every query that needs it — never persisted as a column (see `docs/ADR.md`
    ADR-003) — to avoid staleness if source values change.
  - This value is a *current workload / prioritization signal*, never "automation savings" —
    see Hard requirements below.
- `exploration_recommendations` — one row per AI-generated exploration (bonus path),
  one-to-many from `tasks`: `id`, `task_id` (FK), `recommendation`, `rationale`,
  `verification_points` (JSON-encoded array), `source_weekly_minutes`, `created_at`. Never
  add `automation_score`, `automation_percentage`, `estimated_savings`, or `roi` columns.

## Routes (app/routes.py)

```
GET  /                              Dashboard
GET  /tasks/<task_id>               Task Detail + AI Exploration section
POST /tasks/<task_id>/explorations  Generate + persist an AI exploration (redirects to Task Detail)
GET  /explorations                  Saved Explorations list
GET  /health                        Liveness + SQLite readiness check
```

## Required architecture (from docs/ARCHITECTURE.md)

```
bank_automation_opportunities.csv
  -> Import/Seed command -> Schema + row validation -> SQLite3 (tasks)
  -> Query layer -> {Task Effort, Department Sum, Top 3}
  -> Browser (Flask/Jinja): Dashboard, Task Detail, Saved Explorations (disclaimer on each)

Bonus: Task Detail "Generate AI Exploration" -> app/ai_service.py (sole provider boundary)
       -> OpenRouter (time-boxed company key, see ADR-005) -> structured result
       (recommendation, rationale, verification_points) -> SQLite3 (exploration_recommendations)
       -> displayed on Task Detail and Saved Explorations
```

- Storage is SQLite3 (not DuckDB — see `docs/ADR.md` ADR-002).
- CSV ingestion is a script/command run before the UI is used — there is deliberately no
  CSV-upload UI (out of scope, see SCOPE.md).
- The Web UI must read from persisted SQLite3 data, not recompute from the CSV on every
  request.
- Deployment target is Coolify; the SQLite file must live on persistent storage across
  restarts.
- `app/ai_service.py` is the *only* module allowed to know the AI provider's request/response
  contract (see `docs/ADR.md` ADR-004). It currently calls **OpenRouter**
  (`anthropic/claude-sonnet-4.6` by default) using a **time-boxed company-issued key** as a
  stand-in for the company's own AI endpoint — see ADR-005. Set `AI_API_KEY` (required),
  optionally `AI_ENDPOINT_URL`/`AI_MODEL` to override defaults. Never commit the key or log
  it; it's read only from the environment. Rotate/replace before the key expires (~24h from
  issuance) or before any durable deployment. If `AI_API_KEY` is unset, or the call/response
  fails validation (missing fields, or forbidden savings/ROI/TCO wording anywhere in the
  text), the adapter raises `AIServiceUnavailable` and Task Detail shows an "AI unavailable"
  state — the AI bonus path must fail independently without breaking Dashboard, Task Detail's
  task data, department totals, or Top 3.

## Hard requirements / constraints

From `docs/CONSTRAINTS.md` and `docs/PRD.md`:

- Must never present `weekly_minutes`/Weekly Effort as actual automation savings — the UI
  must carry a visible disclaimer (FR-008 / AC-007). This is a legal/compliance constraint,
  not just a copy nit.
- Ingestion must validate required columns/types before persisting and must reject invalid
  rows explicitly (fail loud) — never silently insert invalid rows (NFR-003).
- No secrets/tokens in the repo; any AI endpoint credential must come from environment
  variables / Coolify-managed secrets.
- No authentication requirement is specified for core analytics — don't add one speculatively.
- Don't invent SLOs, coverage thresholds, or numeric automation-feasibility/savings scores —
  docs intentionally mark these `null` with a named calibration owner rather than guessing.

## Terminology (docs/GLOSSARY.md)

Use these terms consistently in code/UI copy — they were chosen specifically to avoid
implying automation savings:

- **Weekly Effort** — user-facing term for `weekly_runs * minutes_per_run`; technical
  identifier may be `weekly_minutes`.
- **Department Weekly Effort** — sum of Weekly Effort across tasks in a department.
- **Top 3 Task** — the three tasks with highest Weekly Effort in the persisted dataset.
- **Exploration Recommendation** (not "recommendation" alone) — the AI bonus output; must
  not be framed as a decision to automate.
- **Automation Savings** — explicitly *not* computable from this dataset; never equate it
  with Weekly Effort.

## Out of scope (do not build unless requirements change)

CSV upload UI, automation savings/feasibility scoring, user/role management, parsing
customer/project/team identifiers out of `task_name`, editable task CRUD.
