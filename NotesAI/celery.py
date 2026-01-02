import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NotesAI.settings")

app = Celery("NotesAI")

# Load CELERY_ settings from settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover @shared_task in all apps
app.autodiscover_tasks()
