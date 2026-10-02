"""Tests for the Flask routes: Dashboard, Task Detail, Saved Explorations."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module  # noqa: E402
from app import db  # noqa: E402


def seed_db(db_path, tasks):
    db.init_db(db_path)
    conn = db.get_connection(db_path)
    try:
        for task in tasks:
            db.insert_task(conn, task)
        conn.commit()
    finally:
        conn.close()


def make_client(monkeypatch, tmp_path, tasks=None):
    db_path = str(tmp_path / "web.db")
    seed_db(db_path, tasks or [])
    monkeypatch.setenv("DATABASE_PATH", db_path)
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client(), db_path


SAMPLE_TASKS = [
    {"task_id": "T1", "department": "Ops", "task_name": "Task One", "weekly_runs": 10, "minutes_per_run": 5},
    {"task_id": "T2", "department": "Finance", "task_name": "Task Two", "weekly_runs": 2, "minutes_per_run": 3},
]


def test_dashboard_loads(monkeypatch, tmp_path):
    client, _ = make_client(monkeypatch, tmp_path, SAMPLE_TASKS)
    response = client.get("/")
    assert response.status_code == 200
    assert b"Automation Opportunity Finder" in response.data
    assert b"not" in response.data  # disclaimer text present
    assert b"Task One" in response.data


def test_dashboard_empty_state_does_not_crash(monkeypatch, tmp_path):
    client, _ = make_client(monkeypatch, tmp_path, [])
    response = client.get("/")
    assert response.status_code == 200
    assert b"No task data available yet" in response.data


def test_task_detail_shows_task(monkeypatch, tmp_path):
    client, _ = make_client(monkeypatch, tmp_path, SAMPLE_TASKS)
    response = client.get("/tasks/T1")
    assert response.status_code == 200
    assert b"Task One" in response.data
    assert b"No exploration generated yet" in response.data


def test_task_detail_unknown_task_returns_404(monkeypatch, tmp_path):
    client, _ = make_client(monkeypatch, tmp_path, SAMPLE_TASKS)
    response = client.get("/tasks/DOES-NOT-EXIST")
    assert response.status_code == 404
    assert b"Task not found" in response.data


def test_explorations_empty_state(monkeypatch, tmp_path):
    client, _ = make_client(monkeypatch, tmp_path, SAMPLE_TASKS)
    response = client.get("/explorations")
    assert response.status_code == 200
    assert b"No explorations saved yet" in response.data


def test_generate_exploration_persists_and_shows_on_detail_and_list(monkeypatch, tmp_path):
    client, db_path = make_client(monkeypatch, tmp_path, SAMPLE_TASKS)

    def fake_generate(task_context):
        return {
            "recommendation": "Explore this task further.",
            "rationale": "High frequency and moderate duration.",
            "verification_points": ["Check exception rate", "Check input structure"],
        }

    monkeypatch.setattr(app_module.ai_service, "generate_exploration", fake_generate)

    response = client.post("/tasks/T1/explorations", follow_redirects=True)
    assert response.status_code == 200
    assert b"Explore this task further." in response.data
    assert b"Check exception rate" in response.data

    # Persisted: a fresh request (simulating reload) still shows it.
    response = client.get("/tasks/T1")
    assert b"Explore this task further." in response.data

    response = client.get("/explorations")
    assert b"Task One" in response.data


def test_generate_exploration_failure_does_not_break_core_pages(monkeypatch, tmp_path):
    client, _ = make_client(monkeypatch, tmp_path, SAMPLE_TASKS)

    def failing_generate(task_context):
        raise app_module.ai_service.AIServiceUnavailable("endpoint not configured")

    monkeypatch.setattr(app_module.ai_service, "generate_exploration", failing_generate)

    response = client.post("/tasks/T1/explorations")
    assert response.status_code == 200
    assert b"AI unavailable" in response.data

    # Core analytics still work after an AI failure.
    response = client.get("/")
    assert response.status_code == 200
    assert b"Task One" in response.data

    response = client.get("/health")
    assert response.status_code == 200


def test_health_reports_database_reachable(monkeypatch, tmp_path):
    client, _ = make_client(monkeypatch, tmp_path, SAMPLE_TASKS)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"
