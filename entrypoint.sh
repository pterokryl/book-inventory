#!/usr/bin/env bash
set -e

export DJANGO_SQLITE_PATH="${DJANGO_SQLITE_PATH:-/tmp/db.sqlite3}"

if [ ! -f "$DJANGO_SQLITE_PATH" ] && [ -f /app/db.sqlite3 ]; then
  cp /app/db.sqlite3 "$DJANGO_SQLITE_PATH"
fi

python manage.py migrate --noinput

PORT="${PORT:-8080}"
echo "Starting gunicorn on 0.0.0.0:${PORT}"

exec gunicorn book_inventory.wsgi:application \
  --bind "0.0.0.0:${PORT}" \
  --workers 1 \
  --threads 4 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
