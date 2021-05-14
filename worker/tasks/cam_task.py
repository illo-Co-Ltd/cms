import os, sys, inspect
import requests
import json
from random import random
import traceback

import celery
from celery.signals import worker_process_init, worker_process_shutdown
from celery.utils.log import get_logger, get_task_logger
from celery.exceptions import TaskError
from redbeat import RedBeatSchedulerEntry
import time
import datetime, pytz
import cv2

# cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parent = os.path.dirname(cwd)
# sys.path.insert(0, parent)
from cv import camera
from app import app

FLASK_BACKEND = os.environ.get('FLASK_BACKEND')
CAM_MAX_RETRY = 100
CAM_RETRY_INTERVAL = 3

logger = get_task_logger(__name__)
vcam = None


class CaptureTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        self.OperationalError()
        logger.info(f'Task {task_id} suceeded. Sending callback to backend...')
        resp = requests.get(f'{FLASK_BACKEND}/task_callback/on_capture_success/{task_id}')
        logger.info(f'<{resp.status_code}> {resp.text}')

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.warning(f'Task {task_id} failed with exception[{exc}]')


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
        except ValueError:
            continue
        except ConnectionError as e:
            logger.error(traceback.format_exc())
            raise e
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


@app.task(name='cam_task.capture_task', base=CaptureTask)
def capture_task(header: str, data: dict) -> dict:
    try:
        # vcam = camera.VideoCamera()
        if not vcam:
            raise TaskError('Video Camera not initialized')
        else:
            frame = vcam.get_frame()
        ctime = datetime.datetime.now(pytz.timezone("Asia/Seoul"))
        fname = f'{header}_{ctime.strftime("%Y-%m-%dT%H-%M-%S-%f")}.jpg'
        path = f'/data/{fname}'
        res = cv2.imwrite(path, frame)
        body = {
            'target': data.get('target'),
            'path': fname,
            'device': data.get('device'),
            'created': ctime.isoformat(),
            # TODO 요청한 유저로 수정
            'created_by': None,
            'label': data.get('label'),
            # TODO 현재 오프셋 받아오게 수정
            'offset_x': 0,
            'offset_y': 0,
            'offset_z': 0,
            'pos_x': 0,
            'pos_y': 0,
            'pos_z': 0
        }
        if not res:
            raise TaskError('Nothing written by cv2')
        else:
            return body
    except TaskError as e:
        raise e


@app.task(name='cam_task.start_timelapse_task')
def start_timelapse_task(header: str, run_every: float, expire_at: str, data: dict) -> str:
    try:
        interval = celery.schedules.schedule(run_every=run_every)  # seconds
        entry = RedBeatSchedulerEntry(
            'timelapse',
            'cam_task.capture',
            interval,
            args=[header, data],
            app=app
        )
        entry.save()
        return entry.key
    except Exception as e:
        logger.error(traceback.format_exc())
        raise TaskError(e)


@app.task(name='cam_task.stop_timelapse_task')
def stop_timelapse_task(key: str) -> bool:
    try:
        entry = RedBeatSchedulerEntry.from_key(key, app=app)
        entry.delete()
        return True
    except Exception as e:
        logger.error(traceback.format_exc())
        raise TaskError(e)
