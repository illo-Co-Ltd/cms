import os, sys, inspect
import requests
import json
from random import random
import traceback

import celery
from celery.signals import worker_process_init, worker_process_shutdown
from celery.utils.log import get_logger, get_task_logger
from redbeat import RedBeatSchedulerEntry
import time
import datetime, pytz
import cv2

cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent = os.path.dirname(cwd)
sys.path.insert(0, parent)
from cv import camera
from app import app

FLASK_BACKEND = os.environ.get('FLASK_BACKEND')
CAM_MAX_RETRY = 10
CAM_RETRY_INTERVAL = 3

logger = get_task_logger(__name__)
vcam = None


@worker_process_init.connect
def worker_init_handler(**kwargs):
    global vcam
    frame = None
    for i in range(CAM_MAX_RETRY):
        logger.debug(f'Initializing VideoCamera, try #{i + 1}', )
        time.sleep(random() * CAM_RETRY_INTERVAL)
        try:
            vcam = camera.VideoCamera()
            frame = vcam.get_frame()
        except:
            continue
        if frame is not None:
            logger.info(f'VideoCamera initialized (shape):{frame.shape}')
            return
    # TODO 초기화가 불가능하면 해당 worker pool을 종료하도록 구현
    logger.warning(f'Cannot initialize VideoCamera after {CAM_MAX_RETRY} tries')
    raise Exception


@worker_process_shutdown.connect
def worker_shutdown_handler(**kwargs):
    global vcam
    del vcam


@app.task(name='cam_task.capture')
def capture_task(header: str, params: dict) -> (bool, object):
    try:
        # vcam = camera.VideoCamera()
        if not vcam:
            raise Exception('Video Camera not initialized')
        else:
            frame = vcam.get_frame()
        ctime = datetime.datetime.now(pytz.timezone("Asia/Seoul"))
        fname = f'{header}_{ctime.strftime("%Y%m%d-%H%M%S-%f")}.jpg'
        path = f'/data/{fname}'
        res = cv2.imwrite(path, frame)
        if not res:
            raise
        # success -> request callback route
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
        logger.info(data)
        requests.post(f'{FLASK_BACKEND}/api/image', headers=headers, data=json.dumps(data))
        return True, path
    except:
        return False, None


@app.task(name='cam_task.start_timelapse_task')
def start_timelapse_task(header: str, run_every: float, expire_at: str, params: dict) -> (bool, str):
    try:
        interval = celery.schedules.schedule(run_every=run_every)  # seconds
        entry = RedBeatSchedulerEntry(
            'timelapse',
            'cam_task.capture',
            interval,
            args=[header, params],
            app=app
        )
        entry.save()
        return True, entry.key
    except:
        logger.error(traceback.format_exc())
        return False, None


@app.task(name='cam_task.stop_timelapse')
def stop_timelapse_task(key):
    try:
        entry = RedBeatSchedulerEntry.from_key(key)
        entry.delete()
        return True
    except:
        return False
