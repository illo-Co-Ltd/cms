import os, sys, inspect
import requests
import json

cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent = os.path.dirname(cwd)
sys.path.insert(0, parent)

from celery import Task
from app import celery
from redbeat import RedBeatSchedulerEntry
import traceback
import time
import datetime, pytz
import cv2

from cv import camera

FLASK_BACKEND = os.environ.get('FLASK_BACKEND')


class CallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        data = json.dumps({})
        requests.post(f'{FLASK_BACKEND}/api/image', data=data)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


@celery.task(name='cam_task.add')
def add(x: int, y: int, wait: int) -> int:
    time.sleep(wait)
    return x + y


@celery.task(name='cam_task.capture', base=CallbackTask)
def capture(header: str) -> str:
    try:
        cam = camera.VideoCamera()
        frame = cam.get_frame()
        path = f'/data/{header}_{datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y%m%d-%H%M%S")}.jpg'
        res = cv2.imwrite(path, frame)
        if res:
            return path
        else:
            return 'Failed'
    except:
        traceback.print_stack()
        traceback.print_exc()
        return 'Failed'


@celery.task(name='cam_task.periodic_capture')
def periodic_capture(header: str, run_every: float) -> str:
    interval = celery.schedules.schedule(run_every=run_every)  # seconds
    entry = RedBeatSchedulerEntry(
        'periodic_capture',
        'cam_task.capture',
        interval,
        args=[header]
    )
    entry.save()
