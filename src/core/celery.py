from celery import Celery

from core.settings import settings

celery_app = Celery(
    settings.APP_NAME,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.autodiscover_tasks(['tasks'])
