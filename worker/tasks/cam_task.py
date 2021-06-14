import os
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
from .util import check_and_create, refine_path, flatten

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


@app.task(name='cam_task.capture_task')
def capture_task(device, data: dict) -> dict:
    try:
        ctime = datetime.now(pytz.timezone("Asia/Seoul"))

        resp = requests.get(
            f'http://{device.ip}/jpg/',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code != 200:
            raise TaskError(resp)
        resp2 = requests.get(
            f'http://{device.ip}/isp/st_d100.xml',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
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


@app.task(name='cam_task.restore_z')
def restore_z_task(device, *args):
    try:
        resp = requests.get(
            f'http://{device.ip}/isp/appispmu.cgi?btOK=submit&i_mt_dirz={device.last_z}',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code != 200:
            raise TaskError(resp)
    except TaskError as e:
        raise e


@app.task(name='cam_task.move_task')
def move_task(device, x, y, z, *args) -> dict:
    try:
        base = f'http://{device.ip}/isp/appispmu.cgi?btOK=submit'
        params = [f'&i_mt_dir{k}={v}' if v is not None else '' for k, v in {'x': x, 'y': y, 'z': z}.items()]
        resp = requests.get(
            base + ''.join(params),
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code != 200:
            raise TaskError(resp)
    except TaskError as e:
        raise e


@app.task(name='cam_task.offset_task')
def offset_task(device, x, y, z, *args):
    try:
        base = f'http://{device.ip}/isp/appispmu.cgi?btOK=submit'
        params = [f'&i_mt_dir{k}={v}' if v is not None else '' for k, v in {'x': x, 'y': y, 'z': z}.items()]
        resp = requests.get(
            base + ''.join(params),
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code != 200:
            raise TaskError(resp)
    except TaskError as e:
        raise e


def move_and_capture(device, off_x, off_y, off_z, data, *args):
    return [move_task.s(device=device, x=off_x, y=off_y, z=off_z), capture_task.s(device=device, data=data)]


def offset_and_capture(device, off_x, off_y, off_z, data, *args):
    return [offset_task.s(device=device, x=off_x, y=off_y, z=off_z), capture_task.s(device=device, data=data)]


@app.task(name='cam_task.regional_capture', base=M2Task, bind=True)
def regional_capture(self, did, start_x, start_y, end_x, end_y, z, width, height, data):
    try:
        self.did = did
        logger.info(f'Capture from <{(start_x, start_y, z)}> to <{(end_x, end_y, z)}> with distance<{(width, height)}>')
        ncol = ceil((end_x - start_x) / width)
        nrow = ceil((end_y - start_y) / height)
        offx = int((end_x - start_x) / ncol)
        offy = int((end_y - start_y) / nrow)
        # 좌에서 우로 스캔(짝수면 +, 홀수면 -)
        sequence = [None] * (nrow + ncol - 1)
        sequence[::2] = [
            [
                offset_and_capture(self.device, offx * (1 - i % 2 * 2), 0, 0, data) for _ in range(ncol - 1)
            ] for i in range(nrow)
        ]
        sequence[1::2] = [offset_and_capture(self.device, 0, offy, 0, data) for _ in range(nrow - 1)]
        sequence = list(flatten([move_and_capture(self.device, start_x, start_y, z, data)]+sequence))
        sequence.insert(0, restore_z_task.s(self.device))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


@app.task(name='cam_task.printlog')
def printlog(n, a, *args, **kwargs):
    logger.info(f'args: <{args}>')
    logger.info(f'kwargs: <{kwargs}>')
    logger.info(f'this is print <{a}>')
    return n


def unit(maxn, *args, **kwargs):
    logger.info(f'args: <{args}>')
    logger.info(f'kwargs: <{kwargs}>')
    return chain([printlog.s(999, 0)] + [printlog.s(n + 1) for n in range(maxn)])


@app.task(name='cam_task.test', )
def test(*args, **kwargs):
    async_result = regional_capture.s(did=1, start_x=0, start_y=0, end_x=1000, end_y=500, z=2400, width=400,
                                      height=225, data=None).apply_async()
    # async_result = chain([printlog.s(0, 0) for _ in range(3)]).apply_async()
    logger.info(async_result)
