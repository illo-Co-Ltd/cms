import celery
import traceback

from .taskmanager import celery_app
from util import logger


def capture_send(header: str, data: dict):
    name = 'cam_task.capture_task'
    task = celery_app.send_task(name, args=[header, data])
    return task.id


def start_timelapse_send(header: str, run_every: float, expire_at: str, data: dict):
    try:
        task = celery_app.send_task('cam_task.start_timelapse_task', args=[header, run_every, expire_at, data])
        return task.get()
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


def stop_timelapse_send(key):
    try:
        task = celery_app.send_task('cam_task.stop_timelapse_task', args=[key])
        return task.get()
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e
