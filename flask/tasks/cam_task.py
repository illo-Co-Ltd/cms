import os
import celery
from celery import Celery
from . import celeryconfig
from util import logger

BROKER = os.environ.get('BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')

celery_app = Celery('cam_worker')
celery_app.config_from_object(celeryconfig)


def capture_send(header: str, params: dict):
    name = 'cam_task.capture_task'
    task = celery_app.send_task(name, args=[header, params])
    return task.id


def start_timelapse_send(header: str, run_every: float, expire_at: str, params: dict):
    '''
    from redbeat import RedBeatSchedulerEntry
    interval = celery.schedules.schedule(run_every=run_every)  # seconds
    entry = RedBeatSchedulerEntry(
        'timelapse',
        'cam_task.capture',
        interval,
        args=[header, params],
        app=celery_app
    )
    entry.save()
    return True, entry.key
    '''
    task = celery_app.send_task('cam_task.start_timelapse_task', args=[header, run_every, expire_at, params])
    return task.get()


def stop_timelapse_send(key):
    task = celery_app.send_task('cam_task.stop_timelapse_task', args=[key])
    return task.get()
