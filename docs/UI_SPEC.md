# Automation Opportunity Finder — UI_SPEC

Project: `Automation Opportunity Finder`
Document ID: `ui_spec`
Template: `ddd-web-app-v2.8.0`
Status: Draft for implementation
Depends on: `personas`, `prd`, `data_model`, `architecture`

## Surfaces

Three server-rendered pages, no authentication, no SPA navigation:

1. Dashboard — `GET /`
2. Task Detail — `GET /tasks/<task_id>`
3. Saved Explorations — `GET /explorations`

All three share a top navigation bar (`Dashboard` / `Saved Explorations`) and the same
disclaimer copy wherever Weekly Effort is shown: current effort, not estimated Automation
Savings.

### 1. Dashboard (`/`)

Preserves everything already implemented, plus navigation and "View task" actions.

- Top navigation: `Dashboard`, `Saved Explorations`.
- Disclaimer banner (existing copy, unchanged).
- Summary stat cards: tasks tracked, departments, total weekly effort (existing, unchanged).
- Top 3 Tasks by Weekly Effort: existing cards, each gains a `View task` action linking to
  `/tasks/<task_id>`.
- Weekly Effort by Department: existing bar chart, unchanged.
- All Tasks table: existing search/sort/pagination, with a new `Action` column containing a
  `View` link to `/tasks/<task_id>` per row.
- No CSV upload UI, no task CRUD, no automation scoring, no new charts beyond the existing bar
  chart.

### 2. Task Detail (`/tasks/<task_id>`)

New page. Primary surface for the AI-exploration bonus flow.

- Back link to Dashboard.
- Task identity: `task_name`, `department`, `task_id`.
- "Current Workload" block: `weekly_runs`, `minutes_per_run`, computed Weekly Effort
  (human-readable, e.g. "106h 40m / week").
- Disclaimer: Weekly Effort is current effort, not Automation Savings.
- "AI Exploration" section with four states (see below).
- Unknown `task_id`: render a 404 page with a link back to the Dashboard; must not raise an
  unhandled exception.

**AI Exploration section states:**

| State | Trigger | Rendering |
|---|---|---|
| `not_generated` | No `exploration_recommendations` row exists for this task yet | "No exploration generated yet." + `Generate AI Exploration` button (submits `POST /tasks/<task_id>/explorations`) |
| `generating` | Form submitted, request in flight | Not a distinct server-rendered state (synchronous POST → redirect → GET); the button disables on click via a small inline script so a double-submit isn't possible. No separate route/state is implemented for this row in `v1`. |
| `generated` | At least one `exploration_recommendations` row exists | Most recent recommendation shown: `Recommendation`, `Rationale` ("Why investigate"), `Verification Points` as a checklist ("Verify before deciding"), `Generated <timestamp>`. A `Generate AI Exploration` button remains available to add another (history-preserving, per `docs/DATA_MODEL.md`). |
| `error` | AI adapter returns/raises unavailable (missing config, provider error, timeout) | "AI unavailable" message with enough detail to know it's a configuration/connectivity issue, not a verdict on the task. Task data above this section is unaffected. |

### 3. Saved Explorations (`/explorations`)

New page. Lists every persisted `exploration_recommendations` row, newest first.

Columns: Task (name + id, links to `/tasks/<task_id>`), Department, Weekly Effort at the time
of generation (`source_weekly_minutes`, human-readable), Generated timestamp, `View` action
(links to the task's detail page since recommendations are shown there, not on a separate
per-recommendation page in `v1`).

Empty state: "No explorations saved yet." when the table has zero rows — must not crash.

## Critical Path Trace (from `docs/PERSONAS.md`)

| CP-ID | Persona | Critical Action | Where it is satisfied |
|---|---|---|---|
| CP-01 | P-01 | See weekly effort per task from validated, persisted data | Dashboard "All Tasks" table and Task Detail "Current Workload" block — both read from `tasks` via the existing query layer |
| CP-02 | P-01 | See department totals and Top 3 tasks to prioritize quickly | Dashboard "Weekly Effort by Department" and "Top 3 Tasks by Weekly Effort" sections (existing, unchanged) |
| CP-03 | P-02 | Open results in browser and see the disclaimer that current effort is not automation savings | Disclaimer banner present on Dashboard and Task Detail; Saved Explorations shows past effort values with the same framing (never labeled as savings) |

## Explicitly out of scope for these three surfaces

Authentication, CSV upload UI, task CRUD, SPA client-side routing, automation scoring/ROI,
additional charts beyond the department bar chart. (Matches `docs/SCOPE.md`.)

Validation Checklist
- [x] Three surfaces specified: Dashboard, Task Detail, Saved Explorations
- [x] AI states (not generated / generating / generated / error) specified
- [x] CP-01, CP-02, CP-03 traced to a concrete surface/section
- [x] No authentication, CSV upload, CRUD, SPA, or automation scoring introduced
