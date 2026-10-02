# Automation Opportunity Finder — ADR

Project: `Automation Opportunity Finder`
Document ID: `adr`
Template: `ddd-web-app-v2.8.0`
Status: Draft for implementation
Depends on: `architecture`

Each ADR records a decision that is already implemented in this repository, not a proposal.
`adr_status` values used here: `accepted`.

## ADR-001: Server-rendered Flask app instead of a SPA

- Status: accepted
- Context: The exam requirement is a small dashboard that shows task-level weekly effort,
  department totals, and Top 3 tasks, plus (bonus) a page to request and review an AI
  exploration recommendation per task. The repository was empty at the start — no existing
  frontend framework, no client-side state that needs a framework to manage, and a hard time
  budget.
- Alternatives considered:
  - A JS SPA (React/Vue) talking to a JSON API — gives richer client interactivity but adds
    a build step, a second language/toolchain, and API-contract design work that doesn't
    change what the user actually needs (view data, submit one form).
  - A hybrid: server-rendered pages plus a JSON API for later reuse — rejected for now
    because no consumer of that API exists yet; it can be added later without rewriting the
    page templates.
- Decision: Server-rendered Jinja templates with vanilla JavaScript/CSS only (search/sort/
  pagination on the task table; one POST → redirect → GET form for generating an AI
  exploration).
- Positive consequences: smaller surface area, no build pipeline, easy to deploy as a single
  Flask app behind Gunicorn, low implementation risk under the exam's time constraint.
- Negative consequences: no client-side routing or optimistic UI; every navigation is a full
  page load; harder to reuse as a headless API if a future consumer needs one (would require
  adding JSON endpoints alongside the HTML routes).

## ADR-002: SQLite3 instead of DuckDB

- Status: accepted
- Context: The requirement allows either SQLite3 or DuckDB. The dataset is small
  (12,419 rows), and the bonus path needs to persist AI-generated recommendations
  (write-back), not just run analytical scans.
- Alternatives considered:
  - DuckDB — excellent for analytical/OLAP-style scans over larger datasets, but adds a
    second storage engine concern for the write-heavy bonus path (persisting
    `exploration_recommendations`) without a corresponding benefit at this data size.
- Decision: SQLite3 via Python's stdlib `sqlite3`, one database file holding both `tasks`
  and `exploration_recommendations`.
- Positive consequences: zero extra dependency, simple backup/restore (single file), works
  naturally with Flask's request-per-connection pattern, single store for both read-heavy
  analytics and write-heavy recommendations.
- Negative consequences: not optimized for heavy analytical aggregation at much larger scale;
  acceptable per `docs/ARCHITECTURE.md` "Scalability Strategy" which defers that migration
  until data actually grows past what SQLite handles comfortably.

## ADR-003: Weekly Effort computed at query time, never persisted

- Status: accepted
- Context: `weekly_minutes` can be derived from `weekly_runs * minutes_per_run` at any time.
- Alternatives considered:
  - Persist `weekly_minutes` as a column on `tasks`, computed at import time — faster to
    query but creates a second source of truth that can silently go stale if `weekly_runs`
    or `minutes_per_run` are ever corrected without recomputing the derived column.
- Decision: Compute `weekly_minutes` in SQL (`weekly_runs * minutes_per_run`) in every query
  that needs it (`get_all_tasks_with_effort`, `get_department_totals`, `get_top_tasks`); never
  store it as a table column.
- Positive consequences: one formula, enforced in one place; no staleness risk; matches the
  Glossary's explicit requirement that Weekly Effort is derived, not a stored fact.
- Negative consequences: marginally more SQL computation per query; irrelevant at this data
  size (12k rows).

## ADR-004: Server-side AI adapter isolated from core analytics

- Status: accepted
- Context: The AI exploration bonus (FR-010/FR-011) must never put the core dashboard at
  risk, and the company AI endpoint's contract (URL, auth, request/response schema, quota)
  is not yet known.
- Alternatives considered:
  - Call the AI endpoint directly from `app/routes.py` route handlers — couples route logic to a
    specific provider's request/response shape, making it harder to swap providers or run
    tests without live credentials, and risks an AI failure taking down code paths that also
    serve the Dashboard.
- Decision: All AI calls go through a single module, `app/ai_service.py`, exposing one function
  (`generate_exploration(task_context) -> {recommendation, rationale, verification_points}`)
  that `app/routes.py` calls only from the `/tasks/<task_id>/explorations` POST handler. The adapter
  raises/returns a distinct "unavailable" result on any failure (missing config, network
  error, bad response) instead of raising into the Dashboard/task-data code paths.
  The adapter must not invent the provider's actual request/response schema before it is
  confirmed — it defines the interface and an explicit "configuration missing" state instead.
- Positive consequences: Dashboard, Task Detail's own task data, department totals, and
  Top 3 keep working even if the AI endpoint is down or unconfigured; tests can inject a fake
  AI client without touching real quota; provider details can be filled in later in one file.
- Negative consequences: one more module/indirection layer for what is currently a single
  function call; judged worth it given the explicit "AI must fail independently" constraint.

## ADR-005: OpenRouter as a time-boxed stand-in for the company AI endpoint

- Status: accepted
- Context: The company's own AI endpoint contract (URL, auth, model, request/response schema)
  had not been provided when implementation started (see ADR-004). The company separately
  issued a time-boxed (24h) OpenRouter API key for this exercise, scoped to that account's
  own allowed-providers/guardrail configuration.
- Alternatives considered:
  - Continue to only define the interface and raise `AIServiceUnavailable` with no real call —
    satisfies "don't guess the provider contract" but never proves the end-to-end flow
    (persist, redisplay, Saved Explorations) actually works against a real model.
  - Guess at a plausible provider contract — explicitly rejected; would violate
    `docs/CONSTRAINTS.md` and ADR-004.
- Decision: Implement `app/ai_service.py`'s HTTP call against OpenRouter's documented
  chat-completions API (`POST /api/v1/chat/completions`, `Authorization: Bearer <key>`,
  OpenAI-compatible request/response shape) using the company-issued key via the `AI_API_KEY`
  environment variable. This is OpenRouter's own real, documented contract — not invented.
  - Model selection was verified empirically against this account's restrictions, not
    assumed: `openai/gpt-4o-mini` (the original default) is blocked by this account's
    OpenRouter guardrail/allowed-providers setting (confirmed via a direct `404` response
    naming the guardrail). The account's allowed providers are `xai, google-vertex, openai,
    alibaba, minimax, deepseek, anthropic, perplexity, google-ai-studio`. `anthropic/claude-sonnet-4.6`
    was confirmed callable and was set as `AI_MODEL`'s default.
  - Some models (confirmed with `anthropic/claude-sonnet-4.6`) wrap JSON in ```` ```json ````
    code fences despite `response_format: json_object`; `app/ai_service.py` strips this before
    parsing.
  - A content guard rejects any response containing forbidden savings/ROI/TCO/feasibility-%
    wording anywhere in the free text (not just as a JSON key), since prompting alone was
    empirically observed to be insufficient — a real response from this same model included
    "ROI on automation investment would likely be achieved within weeks" in prose on one call.
- Positive consequences: the AI-exploration bonus flow is proven working end-to-end against a
  real model (persist, redisplay on Task Detail, list on Saved Explorations); swapping to the
  company's own endpoint later only requires changing `AI_ENDPOINT_URL`/`AI_API_KEY`/`AI_MODEL`
  and, if its response shape differs from OpenAI-compatible chat-completions, the request/
  response mapping inside `app/ai_service.py` — no other file changes.
- Negative consequences: this key expires ~24h after issuance; it must be rotated or replaced
  with the real company endpoint before relying on this in a durable deployment. The key must
  never be committed to the repository or logged — it is read only from the `AI_API_KEY`
  environment variable at runtime (set via Coolify's environment configuration, not a file in
  version control).

## ADR-006: `expose`, not `ports`, in docker-compose.yaml for Coolify compatibility

- Status: accepted
- Context: The Dockerfile/`docker-compose.yaml` pair is deployed to Coolify (a shared,
  multi-tenant host running many other apps). The first deployment attempt published the app's
  port directly to the host (`ports: ["8000:8000"]`) and failed with "port is already
  allocated" — Coolify's own dashboard was already bound to host port 8000, and any other app
  on the host could just as easily claim whatever port is hardcoded.
- Alternatives considered:
  - Pick a different hardcoded host port — only moves the collision risk to a different
    number; still breaks the moment another app on the shared host picks the same one.
  - Make the host port configurable via an environment variable — still requires every
    deployment to coordinate a unique value by hand; doesn't remove the underlying risk.
- Decision: `docker-compose.yaml` (the file Coolify actually reads and deploys) uses `expose`,
  not `ports`, for the `web` service. Coolify's Traefik proxy reaches the container directly
  over the shared `coolify` Docker network using the exposed port, so no host port binding is
  needed at all on the deployed host. A separate `docker-compose.override.yml` (auto-merged by
  plain `docker compose up`, never read by Coolify) adds `ports: ["8000:8000"]` back for local
  development convenience only.
- Positive consequences: zero host-port collision risk on the shared Coolify server, for this
  app or any other app that might later claim a port; local `docker compose up` still works
  unchanged (`localhost:8000`) via the override file; no coordination needed between
  deployments.
- Negative consequences: one extra file to maintain (`docker-compose.override.yml`); anyone
  reading only `docker-compose.yaml` might wonder how local port access works without also
  knowing Docker Compose auto-merges override files by convention — documented in both files
  and in `CLAUDE.md`.

Validation Checklist
- [x] Each ADR has context, alternatives considered, decision, positive and negative consequences
- [x] All ADRs here describe already-implemented or about-to-be-implemented decisions, not speculative ones
- [x] No ADR invents AI provider contract details that are not yet known
- [x] ADR-005 records that the OpenRouter key is time-boxed and not committed to the repository
