import os

from celery import Celery
from celery.schedules import crontab

# Встановіть стандартний модуль налаштувань Django.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "internal_service_platform.settings")

app = Celery("internal_service_platform")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Завантажувати модулі завдань з усіх зареєстрованих програм Django.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "clear_sessions": {
        "task": "fill_in_docx.tasks.clear_sessions",
        "schedule": crontab(
            hour="2", minute="0", day_of_week="*"
        ),  # Кожен день в 02:00
    },
}
