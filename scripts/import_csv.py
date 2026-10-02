"""Explicit CSV import/seed command.

Usage:
    python scripts/import_csv.py [path-to-csv]

Validates required columns and row values before inserting into SQLite3.
Required columns: task_id, department, task_name, weekly_runs, minutes_per_run

Rejects rows with:
    - missing required values
    - duplicate task_id
    - weekly_runs not a positive integer
    - minutes_per_run not a positive integer

Prints a reconciliation summary: rows read, rows accepted, rows rejected.
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db  # noqa: E402

REQUIRED_COLUMNS = ["task_id", "department", "task_name", "weekly_runs", "minutes_per_run"]

DEFAULT_CSV_PATH = "bank_automation_opportunities.csv"


def _is_positive_int(value: str) -> bool:
    try:
        return int(value) > 0 and str(int(value)) == value.strip()
    except (TypeError, ValueError):
        return False


def validate_row(row: dict, seen_task_ids: set) -> tuple[dict | None, str | None]:
    for column in REQUIRED_COLUMNS:
        value = row.get(column)
        if value is None or str(value).strip() == "":
            return None, f"missing required value for '{column}'"

    task_id = row["task_id"].strip()
    if task_id in seen_task_ids:
        return None, f"duplicate task_id '{task_id}'"

    if not _is_positive_int(row["weekly_runs"]):
        return None, f"weekly_runs must be a positive integer, got '{row['weekly_runs']}'"

    if not _is_positive_int(row["minutes_per_run"]):
        return None, f"minutes_per_run must be a positive integer, got '{row['minutes_per_run']}'"

    task = {
        "task_id": task_id,
        "department": row["department"].strip(),
        "task_name": row["task_name"].strip(),
        "weekly_runs": int(row["weekly_runs"]),
        "minutes_per_run": int(row["minutes_per_run"]),
    }
    return task, None


def import_csv(csv_path: str, database_path: str | None = None) -> dict:
    """Validate and import rows from csv_path into SQLite3.

    Returns a summary dict: rows_read, rows_accepted, rows_rejected, rejections.
    Raises ValueError if the CSV is missing required columns.
    """
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing_columns = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing_columns:
            raise ValueError(f"CSV is missing required columns: {missing_columns}")

        rows_read = 0
        rows_accepted = 0
        rejections = []
        seen_task_ids: set = set()
        accepted_tasks = []

        for row in reader:
            rows_read += 1
            task, error = validate_row(row, seen_task_ids)
            if error:
                rejections.append({"row": rows_read, "reason": error})
                continue
            seen_task_ids.add(task["task_id"])
            accepted_tasks.append(task)
            rows_accepted += 1

    db.init_db(database_path)
    conn = db.get_connection(database_path)
    try:
        for task in accepted_tasks:
            db.insert_task(conn, task)
        conn.commit()
    finally:
        conn.close()

    return {
        "rows_read": rows_read,
        "rows_accepted": rows_accepted,
        "rows_rejected": len(rejections),
        "rejections": rejections,
    }


def main(csv_path: str = DEFAULT_CSV_PATH) -> None:
    summary = import_csv(csv_path)
    print(f"Database path: {db.get_database_path()}")
    print(f"Rows read: {summary['rows_read']}")
    print(f"Imported rows: {summary['rows_accepted']}")
    print(f"Rejected rows: {summary['rows_rejected']}")
    for rejection in summary["rejections"][:20]:
        print(f"  rejected row {rejection['row']}: {rejection['reason']}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV_PATH)
