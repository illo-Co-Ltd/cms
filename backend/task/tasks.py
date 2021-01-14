import os, time
from celery import Celery


BROKER = os.environ.get('BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

celery = Celery(
    'worker',
    broker=BROKER,
    backend=CELERY_BACKEND
)


@celery.task(name='worker.add')
def add(x: int, y: int, wait: int) -> int:
    time.sleep(wait)
    return x + y