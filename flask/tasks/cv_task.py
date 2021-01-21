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


def capture(header: str):
    task = celery_app.send_task('cam_task.capture', args=[header])
    return task.id


def periodic_capture(header: str, run_every: float):
    task = celery_app.send_task('cam_task.periodic_capture', args=[header, run_every])
    return task.id
