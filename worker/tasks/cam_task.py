import os
import time
from math import ceil
import pytz
from datetime import datetime
from contextlib import contextmanager
import traceback
import xml.etree.ElementTree as ETree

import celery
import sqlalchemy
from celery import chain, group
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from celery.signals import worker_process_init, worker_process_shutdown
from celery.utils.log import get_task_logger
from celery.exceptions import TaskError
from redbeat import RedBeatSchedulerEntry
import requests
from requests.auth import HTTPDigestAuth
import cv2
import numpy as np

from app import app
from .util import check_and_create, refine_path, flatten, autofocus, is_stopped

logger = get_task_logger(__name__)
engine = None


class M2Task(celery.Task):
    _device = None

    @contextmanager
    def session_scope(self):
        session = sessionmaker(bind=engine)()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @property
    def device(self):
        if self._device is None:
            with self.session_scope() as session:
                self._device = session.execute(
                    text("SELECT * FROM device WHERE id=:device_id"),
                    {'device_id': self.did}
                ).fetchone()
        return self._device

    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f'Successfully processed <Task {task_id}>.')

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.warning(f'Failed <Task {task_id}> with exception[{exc}]')


@worker_process_init.connect
def worker_init_handler(**kwargs):
    # do some initialization
    global engine
    try:
        engine = sqlalchemy.create_engine(app.conf['mysql_uri'])
        logger.info('Engine initialized.')
    except KeyError as e:
        logger.error('Cannot find mysql_uri.')
        raise e
    except Exception as e:
        logger.error('Something went wrong.')
        raise e


@worker_process_shutdown.connect
def worker_shutdown_handler(**kwargs):
    # do some object deletions
    global engine
    if engine:
        engine.dispose()
        engine = None


@app.task(name='cam_task.capture_task', base=M2Task, bind=True)
def capture_task(self, dummy=None, did=None, focus=None, data=None) -> dict:
    try:
        self.did = did
        ctime = datetime.now(pytz.timezone("Asia/Seoul"))

        if focus is None:
            autofocus(self.device)
            logger.info('Autofocusing...')
            for i in range(3):
                logger.info(3-i)
                time.sleep(1)
        resp = requests.get(
            f'http://{self.device.ip}/jpg/',
            auth=HTTPDigestAuth(self.device.cgi_id, self.device.cgi_pw)
        )
        if resp.status_code != 200:
            raise TaskError(resp)
        resp2 = requests.get(
            f'http://{self.device.ip}/isp/st_d100.xml',
            auth=HTTPDigestAuth(self.device.cgi_id, self.device.cgi_pw)
        )
        if resp2.status_code != 200:
            raise TaskError(resp2)
        resp2.encoding = None
        tree = ETree.fromstring(resp2.text)
        d100 = tree.find('D100')
        curx = d100.find('CURX').text
        cury = d100.find('CURY').text
        curz = d100.find('CURZ').text
        endx = d100.find('ENDX').text
        endy = d100.find('ENDY').text
        endz = d100.find('ENDZ').text

        fname = f'{ctime.strftime("%Y-%m-%dT%H-%M-%S-%f")}.jpg'
        fpath = refine_path(f'/data/{data.get("path")}/{fname}')
        logger.info(fpath)
        check_and_create(os.path.dirname(fpath))

        img = cv2.imdecode(np.frombuffer(resp.content, dtype=np.uint8), -1)
        res = cv2.imwrite(fpath, img)
        if not res:
            raise TaskError('Nothing written by cv2')
        else:
            # save metadata to db
            data = {
                'cell_id': data.get('cell'),
                'path': fpath,
                'device_id': data.get('device'),
                'created': datetime.utcnow(),
                'created_by_id': data.get('created_by_id'),
                'label': data.get('label'),
                'end_x': endx,
                'end_y': endy,
                'end_z': endz,
                'pos_x': curx,
                'pos_y': cury,
                'pos_z': curz
            }
            with self.session_scope() as session:
                session.execute(text(
                    '''INSERT INTO image(cell_id, path, device_id, created, created_by_id, label, end_x, end_y, end_z, pos_x, pos_y, pos_z)
                    VALUES(:cell_id, :path, :device_id, :created, :created_by_id, :label, :end_x, :end_y, :end_z, :pos_x, :pos_y, :pos_z)'''),
                    data)
            return fpath
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


@app.task(name='cam_task.restore_z_task', base=M2Task, bind=True)
def restore_z_task(self, dummy=None, did=None, *args):
    self.did = did
    try:
        resp = requests.get(
            f'http://{self.device.ip}/isp/appispmu.cgi?btOK=submit&i_mt_dirz={self.device.last_z}',
            auth=HTTPDigestAuth(self.device.cgi_id, self.device.cgi_pw)
        )
        if resp.status_code != 200:
            raise TaskError(resp)
    except TaskError as e:
        raise e


@app.task(name='cam_task.move_task', base=M2Task, bind=True)
def move_task(self, dummy=None, did=None, x=None, y=None, z=None, *args) -> dict:
    self.did = did
    logger.info(f'MOVE_TASK X<{x}> Y<{y}> Z<{z}>')
    try:
        base = f'http://{self.device.ip}/isp/appispmu.cgi?btOK=submit'
        params = [f'&i_mt_dir{k}={v}' if v is not None else '' for k, v in {'x': x, 'y': y, 'z': z}.items()]
        resp = requests.get(
            base + ''.join(params),
            auth=HTTPDigestAuth(self.device.cgi_id, self.device.cgi_pw)
        )
        if resp.status_code != 200:
            raise TaskError(resp)
        if is_stopped(self.device, x,y,z):
            return
        else:
            raise TaskError
    except TaskError as e:
        raise e


@app.task(name='cam_task.offset_task', base=M2Task, bind=True)
def offset_task(self, dummy=None, did=None, x=None, y=None, z=None, *args):
    self.did = did
    logger.info(f'OFFSET_TASK X<{x}> Y<{y}> Z<{z}>')
    try:
        resp = requests.get(
            f'http://{self.device.ip}/isp/st_d100.xml',
            auth=HTTPDigestAuth(self.device.cgi_id, self.device.cgi_pw)
        )
        if resp.status_code != 200:
            return False
        resp.encoding = None
        tree = ETree.fromstring(resp.text)
        d100 = tree.find('D100')
        curx = int(d100.find('CURX').text)
        cury = int(d100.find('CURY').text)
        curz = int(d100.find('CURZ').text)

        base = f'http://{self.device.ip}/isp/appispmu.cgi?btOK=submit'
        params = [f'&i_mt_inc{k}={v}' if v is not None else '' for k, v in {'x': x, 'y': y, 'z': z}.items()]
        resp = requests.get(
            base + ''.join(params),
            auth=HTTPDigestAuth(self.device.cgi_id, self.device.cgi_pw)
        )
        if resp.status_code != 200:
            raise TaskError(resp)
        if is_stopped(self.device, curx+x, cury+y, curz+z):
            return
        else:
            raise TaskError
    except TaskError as e:
        raise e


def move_and_capture(off_x, off_y, off_z, focus, data, *args):
    did = data.get('device')
    return [move_task.s(did=did, x=off_x, y=off_y, z=off_z), capture_task.s(did=did, focus=focus, data=data)]


def offset_and_capture(off_x, off_y, off_z, focus, data, *args):
    did = data.get('device')
    return [offset_task.s(did=did, x=off_x, y=off_y, z=off_z), capture_task.s(did=did, focus=focus, data=data)]


@app.task(name='cam_task.regional_capture_task', base=M2Task, bind=True)
def regional_capture_task(self, start_x, start_y, end_x, end_y, z, width, height, focus, data):
    try:
        self.did = data.get('device')
        logger.info(f'Regional capture at device <{self.device.id}>')
        logger.info(f'Capture from <{(start_x, start_y, z)}> to <{(end_x, end_y, z)}> with distance<{(width, height)}>')
        ncol = ceil((end_x - start_x) / width)
        nrow = ceil((end_y - start_y) / height)
        offx = int((end_x - start_x) / ncol)
        offy = int((end_y - start_y) / nrow)
        # 좌에서 우로 스캔(짝수면 +, 홀수면 -)
        sequence = [None] * (2 * nrow - 1)
        sequence[::2] = [
            [
                offset_and_capture(offx * (1 - i % 2 * 2), 0, 0, focus, data) for _ in range(ncol - 1)
            ] for i in range(nrow)
        ]
        sequence[1::2] = [offset_and_capture(0, offy, 0, focus, data) for _ in range(nrow - 1)]
        sequence = list(flatten([move_and_capture(start_x, start_y, z, focus, data)] + sequence))
        sequence.insert(0, restore_z_task.s(did=self.did))
        return chain(sequence).apply_async()
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e
