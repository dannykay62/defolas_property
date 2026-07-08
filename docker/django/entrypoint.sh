#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."

while ! python -c "
import socket
import os

host = os.environ.get('POSTGRES_HOST', 'postgres')
port = int(os.environ.get('POSTGRES_PORT', 5432))

s = socket.socket()
try:
    s.connect((host, port))
    s.close()
except Exception:
    raise SystemExit(1)
"; do
    echo "PostgreSQL is unavailable - sleeping..."
    sleep 2
done

echo "PostgreSQL is up."

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."

exec gunicorn defola_project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -