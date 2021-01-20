import os, sys, inspect

cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent = os.path.dirname(cwd)
sys.path.insert(0, parent)

from app import celery
import traceback
import time
import datetime, pytz
import cv2

from cv import camera


@celery.task(name='cam_task.add')
def add(x: int, y: int, wait: int) -> int:
    time.sleep(wait)
    return x + y


@celery.task(name='cam_task.capture')
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
def periodic_capture(td: datetime.timedelta):
    pass
