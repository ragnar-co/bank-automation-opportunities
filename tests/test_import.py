"""Tests for CSV validation/import."""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db  # noqa: E402
from scripts.import_csv import import_csv, validate_row  # noqa: E402


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def test_missing_required_column_raises(tmp_path):
    csv_path = tmp_path / "bad.csv"
    write_csv(csv_path, ["task_id", "department", "task_name", "weekly_runs"], [])
    db_path = str(tmp_path / "test.db")
    try:
        import_csv(str(csv_path), db_path)
        assert False, "expected ValueError for missing column"
    except ValueError as exc:
        assert "minutes_per_run" in str(exc)


def test_missing_required_value_is_rejected():
    row = {
        "task_id": "T1",
        "department": "",
        "task_name": "Do thing",
        "weekly_runs": "5",
        "minutes_per_run": "10",
    }
    task, error = validate_row(row, set())
    assert task is None
    assert "department" in error


def test_duplicate_task_id_is_rejected():
    row = {
        "task_id": "T1",
        "department": "Ops",
        "task_name": "Do thing",
        "weekly_runs": "5",
        "minutes_per_run": "10",
    }
    task, error = validate_row(row, {"T1"})
    assert task is None
    assert "duplicate" in error


def test_invalid_weekly_runs_is_rejected():
    row = {
        "task_id": "T1",
        "department": "Ops",
        "task_name": "Do thing",
        "weekly_runs": "-5",
        "minutes_per_run": "10",
    }
    task, error = validate_row(row, set())
    assert task is None
    assert "weekly_runs" in error

    row["weekly_runs"] = "abc"
    task, error = validate_row(row, set())
    assert task is None
    assert "weekly_runs" in error


def test_invalid_minutes_per_run_is_rejected():
    row = {
        "task_id": "T1",
        "department": "Ops",
        "task_name": "Do thing",
        "weekly_runs": "5",
        "minutes_per_run": "0",
    }
    task, error = validate_row(row, set())
    assert task is None
    assert "minutes_per_run" in error


def test_valid_rows_are_imported_and_persisted(tmp_path):
    csv_path = tmp_path / "ok.csv"
    write_csv(
        csv_path,
        ["task_id", "department", "task_name", "weekly_runs", "minutes_per_run"],
        [
            ["T1", "Ops", "Task One", "5", "10"],
            ["T2", "Finance", "Task Two", "2", "3"],
            ["T1", "Ops", "Duplicate of T1", "1", "1"],
            ["T3", "Finance", "Missing runs", "", "5"],
        ],
    )
    db_path = str(tmp_path / "test.db")

    summary = import_csv(str(csv_path), db_path)

    assert summary["rows_read"] == 4
    assert summary["rows_accepted"] == 2
    assert summary["rows_rejected"] == 2

    conn = db.get_connection(db_path)
    try:
        count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        assert count == 2
    finally:
        conn.close()
