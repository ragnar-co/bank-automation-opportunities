FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DATABASE_PATH=/data/app.db
ENV PORT=8000

EXPOSE 8000

# Idempotent import: only seed the DB if it does not already exist, then start Gunicorn.
CMD ["sh", "-c", "test -f \"$DATABASE_PATH\" || python scripts/import_csv.py; gunicorn --bind 0.0.0.0:$PORT app:app"]
