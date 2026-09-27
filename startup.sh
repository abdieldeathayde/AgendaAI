#!/usr/bin/env bash
set -e

export PORT="${PORT:-80}"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn app:app --bind 0.0.0.0:${PORT} --workers 2 --timeout 120
