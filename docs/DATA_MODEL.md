# Automation Opportunity Finder — DATA_MODEL

Project: `Automation Opportunity Finder`
Document ID: `data_model`
Template: `ddd-web-app-v2.8.0`
Status: Draft for implementation
Depends on: `architecture`, `constraints`, `glossary`

This document is the canonical owner of schema/entity names. `docs/GLOSSARY.md`'s
Term-to-Entity Mapping must match this document; where they disagree, this document wins.

## Entities

### `tasks`

One row per validated task imported from `bank_automation_opportunities.csv`.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `task_id` | TEXT | PRIMARY KEY | Source CSV `task_id`; unique per AC-002 |
| `department` | TEXT | NOT NULL | Source CSV `department` |
| `task_name` | TEXT | NOT NULL | Source CSV `task_name` |
| `weekly_runs` | INTEGER | NOT NULL, > 0 | Validated positive integer at import time |
| `minutes_per_run` | INTEGER | NOT NULL, > 0 | Validated positive integer at import time |

`weekly_minutes` (Weekly Effort) is **not** a column — it is always computed at query time as
`weekly_runs * minutes_per_run` (see `docs/ADR.md` ADR-003).

### `exploration_recommendations`

One row per AI-generated exploration recommendation for a task. A task may have zero or many
rows here (one-to-many from `tasks`), so recommendation history is preserved rather than
overwritten on regeneration.

| Column | Type | Constraints | Notes |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Surrogate key |
| `task_id` | TEXT | NOT NULL, FOREIGN KEY -> `tasks(task_id)` | Owning task |
| `recommendation` | TEXT | NOT NULL | AI-generated recommendation text |
| `rationale` | TEXT | NOT NULL | AI-generated rationale text |
| `verification_points` | TEXT | NOT NULL | JSON-encoded array of strings (SQLite has no native array type) |
| `source_weekly_minutes` | INTEGER | NOT NULL | Weekly Effort of the task at the moment this recommendation was generated, so historical rows remain interpretable if the task's own `weekly_runs`/`minutes_per_run` change later |
| `created_at` | TEXT | NOT NULL | ISO-8601 UTC timestamp, set by the application at insert time |

Explicitly **not** modeled, per `docs/CONSTRAINTS.md` and `docs/SCOPE.md`: `automation_score`,
`automation_percentage`, `estimated_savings`, `roi`. No column may represent a claimed or
estimated automation saving — only current workload (`tasks`) and AI-proposed exploration
reasoning (`exploration_recommendations`).

## Relationships

```text
tasks (1) ----< (many) exploration_recommendations
  task_id                  task_id (FK)
```

- Deleting a task is out of scope (no task CRUD, per `docs/SCOPE.md`); no cascade behavior is
  defined because tasks are never deleted by the application.

## Term-to-Entity Mapping (canonical; supersedes `docs/GLOSSARY.md` until that file is reconciled)

| Term (Glossary) | Entity | Notes |
|---|---|---|
| Task | `tasks` | |
| Weekly Effort | computed `weekly_runs * minutes_per_run` | not a stored column |
| Exploration Recommendation | `exploration_recommendations` | supersedes the earlier placeholder name `ai_recommendations` |

## Confidentiality / PDPA

- `pdpa_classification`, `confidentiality_class`: `null` — calibration owner: Product/Legal
  reviewer, consistent with `docs/CONSTRAINTS.md`. The dataset as provided contains task
  metadata, not identifiable personal data about customers or employees; this has not been
  through a formal legal review.

Validation Checklist
- [x] `tasks` schema matches `app/db.py`'s implemented `SCHEMA`
- [x] `exploration_recommendations` has no automation-savings/ROI/feasibility-score column
- [x] One-to-many relationship from `tasks` to `exploration_recommendations` is explicit
- [x] This document, not GLOSSARY.md, is the canonical entity-name owner
