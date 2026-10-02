"""Automation Opportunity Finder — Flask application entrypoint.

Routes:
    GET /        dashboard: task weekly effort, department totals, top 3
    GET /health  liveness/readiness check for container deployment
"""

from flask import Flask, render_template

import db

app = Flask(__name__)


@app.template_filter("human_minutes")
def human_minutes(total_minutes):
    """Render a minute count as e.g. '12h 5m' for readability."""
    total_minutes = int(total_minutes or 0)
    hours, minutes = divmod(total_minutes, 60)
    if hours and minutes:
        return f"{hours}h {minutes}m"
    if hours:
        return f"{hours}h"
    return f"{minutes}m"


@app.route("/health")
def health():
    return {"status": "ok"}, 200


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


if __name__ == "__main__":
    app.run(debug=True)
