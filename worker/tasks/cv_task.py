import os, sys, inspect
import requests
import json

cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent = os.path.dirname(cwd)
sys.path.insert(0, parent)

from celery.signals import worker_init, worker_shutdown
from app import celery
from redbeat import RedBeatSchedulerEntry
import traceback
import time
import datetime, pytz
import cv2

from cv import camera

FLASK_BACKEND = os.environ.get('FLASK_BACKEND')
vcam = None


@worker_init.connect
def worker_init_handler(**kwargs):
    global vcam
    vcam = camera.VideoCamera()


@worker_shutdown.connect
def worker_shutdown_handler(**kwargs):
    global vcam
    del vcam


@celery.task(name='cam_task.add')
def add(x: int, y: int, wait: int) -> int:
    time.sleep(wait)
    return x + y


@celery.task(name='cam_task.capture')
def capture(header: str, params: dict) -> str:
    try:
        frame = vcam.get_frame()
        ctime = datetime.datetime.now(pytz.timezone("Asia/Seoul"))
        fname = f'{header}_{ctime.strftime("%Y%m%d-%H%M%S-%f")}.jpg'
        path = f'/data/{fname}'
        res = cv2.imwrite(path, frame)
        if res:  # success -> request callback route
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            data = {
                'target': params.get('target'),
                'path': fname,
                'device': params.get('device'),
                'created': ctime.timestamp(),
                # TODO 요청한 유저로 수정
                'created_by': None,
                'label': params.get('label'),
                # TODO 현재 오프셋 받아오게 수정
                'offset_x': 0,
                'offset_y': 0,
                'offset_z': 0,
                'pos_x': 0,
                'pos_y': 0,
                'pos_z': 0
            }
            print(data)
            print(type(data))
            requests.post(f'{FLASK_BACKEND}/api/image', headers=headers, data=json.dumps(data))
            return path
        else:
            return 'Failed'
    except:
        traceback.print_stack()
        traceback.print_exc()
        return 'Failed'


@celery.task(name='cam_task.periodic_capture')
def periodic_capture(header: str, run_every: float, expire_at: str, params: dict) -> str:
    interval = celery.schedules.schedule(run_every=run_every)  # seconds
    entry = RedBeatSchedulerEntry(
        'periodic_capture',
        'cam_task.capture',
        interval,
        args=[header, params]
    )
    entry.save()
