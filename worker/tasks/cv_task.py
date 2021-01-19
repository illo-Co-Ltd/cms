import os
import time
import datetime, pytz
from celery import Celery
import cv2

from cv import camera

BROKER = os.environ.get('BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')

celery = Celery(
    'cv_worker',
    broker=BROKER,
    backend=CELERY_BACKEND
)


@celery.task(name='cam_task.add')
def add(x: int, y: int, wait: int) -> int:
    time.sleep(wait)
    return x + y


@celery.task(name='cam_task.capture')
def capture(header: str):
    try:
        cam = camera.VideoCamera()
        frame = cam.get_frame()
        path = f'/data/{header}_{datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y%m%d-%H%M%S")}.jpg'
        res = cv2.imwrite(path, frame)
        if res:
            return path
        else:
            return 'Failed'

    except Exception as e:
        return 'Failed'


@celery.task(name='cam_task.periodic_capture')
def periodic_capture():
    pass
