from AgendaAI.wsgi import application

# Compatibility alias for Render / Gunicorn default startup command:
# gunicorn app:app
app = application
