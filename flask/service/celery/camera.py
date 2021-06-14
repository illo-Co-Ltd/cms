import traceback

from celery import Signature

from .taskmanager import celery_app
from util.logger import logger


def test_connection():
    return celery_app.send_task('test_task.connection_test', args=['Hello']).get()


def send_capture(data: dict):
    name = 'cam_task.capture_task'
    task = celery_app.send_task(name, args=[data])
    return task.id


def send_regional_capture(start_x, start_y, end_x, end_y, z, width, height, data):
    try:
        task = celery_app.send_task(
            'cam_task.regional_capture_task',
            args=[start_x, start_y, end_x, end_y, z, width, height, data]
        )
        return task.id
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


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


def chain_test():
    celery_app.send_task(
        'cam_task.test1',
        chain=[
            Signature('cam_task.test2'),
            Signature('cam_task.test3')
        ]
    )
