"""SQLite3 access layer for the Automation Opportunity Finder.

Schema, connection handling, and query functions. weekly_minutes is never
persisted as a column — it is always computed at query time as
weekly_runs * minutes_per_run, per docs/ARCHITECTURE.md.
"""

import os
import sqlite3

DEFAULT_DATABASE_PATH = os.path.join("data", "app.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    department TEXT NOT NULL,
    task_name TEXT NOT NULL,
    weekly_runs INTEGER NOT NULL,
    minutes_per_run INTEGER NOT NULL
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
        conn.execute(SCHEMA)
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
