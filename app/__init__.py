"""Automation Opportunity Finder — Flask application package.

The Flask instance is created here (not via a factory function) so
`gunicorn app:app` and `from app import app` both resolve to it directly.
`templates/` and `static/` stay at the project root (not inside this
package) — see docs/ADR.md — so they are wired up explicitly below.

Routes live in app/routes.py and are imported at the bottom of this file to
avoid a circular import (routes.py needs the `app` object defined here).
"""

import os

from flask import Flask, render_template

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, "templates"),
    static_folder=os.path.join(PROJECT_ROOT, "static"),
)


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


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


from app import routes  # noqa: E402,F401
