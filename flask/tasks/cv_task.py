import os
from celery import Celery

BROKER = os.environ.get('BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')

celery_app = Celery(
    'cv_worker',
    broker=BROKER,
    backend=CELERY_BACKEND
)


def add(x: int, y: int, wait: int) -> int:
    task = celery_app.send_task('cam_task.add', args=[x, y, wait])
    return task.id


def add_result(task_id: int) -> int:
    task = celery_app.AsyncResult(task_id)
    value = [value for result, value in task.collect()]
    return value


def capture(header: str, params: dict):
    task = celery_app.send_task('cam_task.capture', args=[header, params])
    return task.id


def periodic_capture(header: str, run_every: float, expire_at: str, params: dict):
    task = celery_app.send_task('cam_task.periodic_capture', args=[header, run_every, expire_at, params])
    return task.id
