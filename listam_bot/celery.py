import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listam_bot.settings")

app = Celery("listam_bot")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
