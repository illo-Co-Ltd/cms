import traceback

from .taskmanager import celery_app
from util import logger


def send_capture(data: dict):
    name = 'cam_task.capture_task'
    task = celery_app.send_task(name, args=[data])
    return task.id


def send_start_timelapse(header: str, run_every: float, expire_at: str, data: dict):
    try:
        task = celery_app.send_task('cam_task.start_timelapse_task', args=[header, run_every, expire_at, data])
        return task.get()
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


def send_stop_timelapse(key):
    try:
        task = celery_app.send_task('cam_task.stop_timelapse_task', args=[key])
        return task.get()
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e
