import multiprocessing
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

workers = max(2, multiprocessing.cpu_count() // 2)
bind = "0.0.0.0:8000"
worker_class = "sync"
threads = 2
timeout = 120
keepalive = 5
preload_app = True

django_settings = "AgendaAI.settings"

accesslog = str(BASE_DIR / "gunicorn-access.log")
errorlog = str(BASE_DIR / "gunicorn-error.log")
loglevel = "info"

def when_ready(server):
    server.log.info("AgendaAI iniciado em 0.0.0.0:8000")
