#!/bin/sh
set -e

if [ -n "$DB_HOST" ]; then
    echo "Aguardando banco de dados ($DB_HOST:${DB_PORT:-3306})..."
    python - <<'PY'
import sys, time, os, socket
host = os.environ.get("DB_HOST", "db")
port = int(os.environ.get("DB_PORT", "3306"))
start = time.time()
while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"Banco de dados acessível em {host}:{port}!")
            break
    except OSError:
        if time.time() - start > 90:
            print("Tempo esgotado aguardando banco de dados.", file=sys.stderr)
            sys.exit(1)
        time.sleep(1)
PY
fi

echo "Executando migrações do banco de dados..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Em produção (Render/Docker), use Gunicorn e a porta fornecida pelo ambiente.
if [ "${DJANGO_RUNSERVER:-0}" = "1" ]; then
    exec python manage.py runserver "0.0.0.0:${PORT:-8000}"
fi

exec gunicorn AgendaAI.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers "${WEB_CONCURRENCY:-2}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    --access-logfile -
