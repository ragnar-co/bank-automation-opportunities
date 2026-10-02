"""SQLite3 access layer for the Automation Opportunity Finder.

Schema, connection handling, and query functions. weekly_minutes is never
persisted as a column — it is always computed at query time as
weekly_runs * minutes_per_run, per docs/ARCHITECTURE.md and docs/ADR.md (ADR-003).

Canonical schema ownership: docs/DATA_MODEL.md.
"""

import json
import os
import sqlite3
from datetime import datetime, timezone

DEFAULT_DATABASE_PATH = os.path.join("data", "app.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    department TEXT NOT NULL,
    task_name TEXT NOT NULL,
    weekly_runs INTEGER NOT NULL,
    minutes_per_run INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS exploration_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL REFERENCES tasks(task_id),
    recommendation TEXT NOT NULL,
    rationale TEXT NOT NULL,
    verification_points TEXT NOT NULL,
    source_weekly_minutes INTEGER NOT NULL,
    created_at TEXT NOT NULL
);
"""


def get_database_path() -> str:
    return os.environ.get("DATABASE_PATH", DEFAULT_DATABASE_PATH)


def get_connection(database_path: str | None = None) -> sqlite3.Connection:
    path = database_path or get_database_path()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(database_path: str | None = None) -> None:
    """Create the tasks table if it does not exist."""
    conn = get_connection(database_path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def insert_task(conn: sqlite3.Connection, task: dict) -> None:
    conn.execute(
        """
        INSERT INTO tasks (task_id, department, task_name, weekly_runs, minutes_per_run)
        VALUES (:task_id, :department, :task_name, :weekly_runs, :minutes_per_run)
        """,
        task,
    )


def get_all_tasks_with_effort(conn: sqlite3.Connection) -> list[dict]:
    """Return every task with weekly_minutes = weekly_runs * minutes_per_run."""
    rows = conn.execute(
        """
        SELECT task_id, department, task_name, weekly_runs, minutes_per_run,
               weekly_runs * minutes_per_run AS weekly_minutes
        FROM tasks
        ORDER BY weekly_minutes DESC
        """
    ).fetchall()
    return [dict(row) for row in rows]


def get_department_totals(conn: sqlite3.Connection) -> list[dict]:
    """Return total weekly_minutes grouped by department."""
    rows = conn.execute(
        """
        SELECT department, SUM(weekly_runs * minutes_per_run) AS weekly_minutes
        FROM tasks
        GROUP BY department
        ORDER BY weekly_minutes DESC
        """
    ).fetchall()
    return [dict(row) for row in rows]


def get_top_tasks(conn: sqlite3.Connection, limit: int = 3) -> list[dict]:
    """Return the top N tasks ordered by weekly_minutes DESC."""
    rows = conn.execute(
        """
        SELECT task_id, department, task_name, weekly_runs, minutes_per_run,
               weekly_runs * minutes_per_run AS weekly_minutes
        FROM tasks
        ORDER BY weekly_minutes DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


def get_task(conn: sqlite3.Connection, task_id: str) -> dict | None:
    """Return a single task with computed weekly_minutes, or None if not found."""
    row = conn.execute(
        """
        SELECT task_id, department, task_name, weekly_runs, minutes_per_run,
               weekly_runs * minutes_per_run AS weekly_minutes
        FROM tasks
        WHERE task_id = ?
        """,
        (task_id,),
    ).fetchone()
    return dict(row) if row else None


def save_exploration(
    conn: sqlite3.Connection,
    task_id: str,
    recommendation: str,
    rationale: str,
    verification_points: list[str],
    source_weekly_minutes: int,
) -> int:
    """Persist a generated exploration recommendation for a task. Returns its id."""
    created_at = datetime.now(timezone.utc).isoformat()
    cursor = conn.execute(
        """
        INSERT INTO exploration_recommendations
            (task_id, recommendation, rationale, verification_points, source_weekly_minutes, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            task_id,
            recommendation,
            rationale,
            json.dumps(verification_points),
            source_weekly_minutes,
            created_at,
        ),
    )
    conn.commit()
    return cursor.lastrowid


def _row_to_exploration(row: sqlite3.Row) -> dict:
    exploration = dict(row)
    exploration["verification_points"] = json.loads(exploration["verification_points"])
    return exploration


def get_explorations_for_task(conn: sqlite3.Connection, task_id: str) -> list[dict]:
    """Return every saved exploration for a task, newest first."""
    rows = conn.execute(
        """
        SELECT id, task_id, recommendation, rationale, verification_points,
               source_weekly_minutes, created_at
        FROM exploration_recommendations
        WHERE task_id = ?
        ORDER BY created_at DESC, id DESC
        """,
        (task_id,),
    ).fetchall()
    return [_row_to_exploration(row) for row in rows]


def get_all_explorations(conn: sqlite3.Connection) -> list[dict]:
    """Return every saved exploration across all tasks, newest first, joined with task info."""
    rows = conn.execute(
        """
        SELECT er.id, er.task_id, er.recommendation, er.rationale, er.verification_points,
               er.source_weekly_minutes, er.created_at,
               t.task_name, t.department
        FROM exploration_recommendations er
        JOIN tasks t ON t.task_id = er.task_id
        ORDER BY er.created_at DESC, er.id DESC
        """
    ).fetchall()
    return [_row_to_exploration(row) for row in rows]
