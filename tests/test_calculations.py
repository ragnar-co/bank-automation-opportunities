"""Tests for weekly effort calculations/aggregation."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import db  # noqa: E402


def seed(db_path, tasks):
    db.init_db(db_path)
    conn = db.get_connection(db_path)
    try:
        for task in tasks:
            db.insert_task(conn, task)
        conn.commit()
    finally:
        conn.close()


def test_weekly_minutes_calculation(tmp_path):
    db_path = str(tmp_path / "calc.db")
    seed(
        db_path,
        [
            {"task_id": "T1", "department": "Ops", "task_name": "A", "weekly_runs": 5, "minutes_per_run": 10},
            {"task_id": "T2", "department": "Ops", "task_name": "B", "weekly_runs": 3, "minutes_per_run": 7},
        ],
    )
    conn = db.get_connection(db_path)
    try:
        tasks = {t["task_id"]: t for t in db.get_all_tasks_with_effort(conn)}
    finally:
        conn.close()

    assert tasks["T1"]["weekly_minutes"] == 50
    assert tasks["T2"]["weekly_minutes"] == 21


def test_department_aggregation(tmp_path):
    db_path = str(tmp_path / "dept.db")
    seed(
        db_path,
        [
            {"task_id": "T1", "department": "Ops", "task_name": "A", "weekly_runs": 5, "minutes_per_run": 10},
            {"task_id": "T2", "department": "Ops", "task_name": "B", "weekly_runs": 3, "minutes_per_run": 7},
            {"task_id": "T3", "department": "Finance", "task_name": "C", "weekly_runs": 2, "minutes_per_run": 2},
        ],
    )
    conn = db.get_connection(db_path)
    try:
        totals = {d["department"]: d["weekly_minutes"] for d in db.get_department_totals(conn)}
    finally:
        conn.close()

    assert totals["Ops"] == 50 + 21
    assert totals["Finance"] == 4


def test_top_3_ordering(tmp_path):
    db_path = str(tmp_path / "top3.db")
    seed(
        db_path,
        [
            {"task_id": "T1", "department": "Ops", "task_name": "A", "weekly_runs": 1, "minutes_per_run": 1},
            {"task_id": "T2", "department": "Ops", "task_name": "B", "weekly_runs": 100, "minutes_per_run": 1},
            {"task_id": "T3", "department": "Ops", "task_name": "C", "weekly_runs": 50, "minutes_per_run": 1},
            {"task_id": "T4", "department": "Ops", "task_name": "D", "weekly_runs": 10, "minutes_per_run": 1},
        ],
    )
    conn = db.get_connection(db_path)
    try:
        top = db.get_top_tasks(conn, limit=3)
    finally:
        conn.close()

    assert [t["task_id"] for t in top] == ["T2", "T3", "T4"]
    assert top[0]["weekly_minutes"] >= top[1]["weekly_minutes"] >= top[2]["weekly_minutes"]
