# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project state

This repository is currently **pre-implementation**: it contains only the source dataset
(`bank_automation_opportunities.csv`) and a design-document set (`docs/`). There is no
application code, build tooling, or test suite yet. The framework/runtime, deployment
command, and several other details are explicitly left as `null` in the docs below, pending
a developer decision — check `docs/ARCHITECTURE.md` before assuming a stack.

## What this project is

"Automation Opportunity Finder" — a web app that ingests the CSV of recurring task data,
validates and persists it to SQLite3, and shows which tasks/departments consume the most
recurring weekly time, so management can prioritize what to explore for automation next.

Read these in order before implementing anything; each has a `Depends on` field at the top
describing the chain: `docs/CONSTRAINTS.md` → `docs/PERSONAS.md` / `docs/VPD.md` →
`docs/SCOPE.md` → `docs/PRD.md` → `docs/ARCHITECTURE.md` → `docs/GLOSSARY.md`.

## Core data model

CSV columns (`bank_automation_opportunities.csv`, ~12,419 rows, 8 departments):
`task_id, department, task_name, weekly_runs, minutes_per_run`

- **Weekly Effort** (`weekly_minutes`) = `weekly_runs * minutes_per_run`, computed at query
  time, not persisted as a column — avoids staleness if source values change
  (see ARCHITECTURE.md "Tech Stack Decisions").
- `task_id` must be unique (primary key) after ingestion.
- This value is a *current workload / prioritization signal*, never "automation savings" —
  see the Legal/Compliance constraint below.

## Required architecture (from docs/ARCHITECTURE.md)

```
bank_automation_opportunities.csv
  -> Import/Seed command -> Schema + row validation -> SQLite3
  -> Query layer -> {Task Effort, Department Sum, Top 3} -> Web UI (with disclaimer)

Bonus: SQLite3 aggregates -> Company AI endpoint -> exploration recommendation
       -> persisted in SQLite3 -> displayed in Web UI
```

- Storage is SQLite3 (not DuckDB — chosen for low setup overhead and because the bonus path
  needs write-back into the same store as the raw tasks).
- CSV ingestion is a script/command run before the UI is used — there is deliberately no
  CSV-upload UI (out of scope, see SCOPE.md).
- The Web UI must read from persisted SQLite3 data, not recompute from the CSV on every
  request.
- Deployment target is Coolify; the SQLite file must live on persistent storage across
  restarts.
- The AI bonus path (company AI endpoint) must fail independently without breaking core
  analytics.

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
