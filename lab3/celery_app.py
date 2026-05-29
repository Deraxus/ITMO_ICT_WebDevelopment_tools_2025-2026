from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "travel_buddy_parser",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
    enable_utc=True,
)

# Пример periodic task для задания: раз в час обновляем данные с example.com.
celery_app.conf.beat_schedule = {
    "parse-example-page-every-hour": {
        "task": "app.tasks.parse_url_task",
        "schedule": 3600.0,
        "args": ("https://example.com",),
    },
}
