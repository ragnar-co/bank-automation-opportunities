"""Local development entrypoint: python run.py

Production uses Gunicorn against the `app` package directly:
    gunicorn --bind 0.0.0.0:$PORT app:app
"""

from app import app

if __name__ == "__main__":
    app.run(debug=True)
