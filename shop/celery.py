import os

from celery import Celery
from celery.beat import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')

app = Celery('shop')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     "send_report": {
#         "task": "users.tasks.send_report",
#         "schedule": crontab(minute="*/1")
#         # "schedule": crontab(month_of_year=3, day_of_month=10, hour=18, minute=45)
#     }
# }

app.conf.beat_schedule = {
    "print-hello-every-minute": {
        "task": "users.tasks.print_hello",
        "schedule": crontab(minute="*"),
    },
}