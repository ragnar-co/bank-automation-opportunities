"""Route handlers for the Automation Opportunity Finder.

Routes:
    GET  /                              dashboard: task weekly effort, department totals, top 3
    GET  /tasks/<task_id>               task detail + AI exploration
    POST /tasks/<task_id>/explorations  generate and persist an AI exploration for a task
    GET  /explorations                  saved explorations list
    GET  /health                        liveness + SQLite readiness check for container deployment
"""

import sqlite3

from flask import abort, redirect, render_template, url_for

from app import ai_service, app, db


@app.route("/health")
def health():
    """Liveness + readiness: process is up AND SQLite is reachable/queryable."""
    try:
        conn = db.get_connection()
        try:
            conn.execute("SELECT 1").fetchone()
        finally:
            conn.close()
    except sqlite3.Error as exc:
        return {"status": "degraded", "database": "unreachable", "error": str(exc)}, 503

    return {"status": "ok", "database": "reachable"}, 200


@app.route("/")
def index():
    conn = db.get_connection()
    try:
        tasks = db.get_all_tasks_with_effort(conn)
        department_totals = db.get_department_totals(conn)
        top_tasks = db.get_top_tasks(conn, limit=3)
    finally:
        conn.close()

    max_department_minutes = max((d["weekly_minutes"] for d in department_totals), default=0)
    summary = {
        "task_count": len(tasks),
        "department_count": len(department_totals),
        "total_weekly_minutes": sum(t["weekly_minutes"] for t in tasks),
    }

    return render_template(
        "index.html",
        tasks=tasks,
        department_totals=department_totals,
        top_tasks=top_tasks,
        max_department_minutes=max_department_minutes,
        summary=summary,
    )


@app.route("/tasks/<task_id>")
def task_detail(task_id):
    conn = db.get_connection()
    try:
        task = db.get_task(conn, task_id)
        if task is None:
            abort(404)
        explorations = db.get_explorations_for_task(conn, task_id)
    finally:
        conn.close()

    return render_template("task_detail.html", task=task, explorations=explorations)


@app.route("/tasks/<task_id>/explorations", methods=["POST"])
def create_exploration(task_id):
    conn = db.get_connection()
    try:
        task = db.get_task(conn, task_id)
        if task is None:
            abort(404)

        try:
            result = ai_service.generate_exploration(
                {
                    "task_id": task["task_id"],
                    "department": task["department"],
                    "task_name": task["task_name"],
                    "weekly_runs": task["weekly_runs"],
                    "minutes_per_run": task["minutes_per_run"],
                    "weekly_minutes": task["weekly_minutes"],
                }
            )
        except ai_service.AIServiceUnavailable as exc:
            return render_template(
                "task_detail.html",
                task=task,
                explorations=db.get_explorations_for_task(conn, task_id),
                ai_error=str(exc),
            )

        db.save_exploration(
            conn,
            task_id=task["task_id"],
            recommendation=result["recommendation"],
            rationale=result["rationale"],
            verification_points=result["verification_points"],
            source_weekly_minutes=task["weekly_minutes"],
        )
    finally:
        conn.close()

    return redirect(url_for("task_detail", task_id=task_id))


@app.route("/explorations")
def explorations():
    conn = db.get_connection()
    try:
        all_explorations = db.get_all_explorations(conn)
    finally:
        conn.close()

    return render_template("explorations.html", explorations=all_explorations)
