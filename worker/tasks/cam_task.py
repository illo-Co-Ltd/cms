import os
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
from .util import check_and_create, refine_path

logger = get_task_logger(__name__)
engine = None


class M2Task(celery.Task):
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
        with self.session_scope() as session:
            return session.execute(
                text("SELECT * FROM device WHERE id=:device_id"),
                {'device_id': self.did}
            ).fetchone()

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
def capture_task(self, data: dict) -> dict:
    try:
        self.data = data
        ctime = datetime.now(pytz.timezone("Asia/Seoul"))

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


@app.task(name='cam_task.move_task', base=M2Task, bind=True)
def move_task(self, did, x, y, z) -> dict:
    try:
        self.did = did
        resp = requests.get(
            f'http://{self.device.ip}/isp/appispmu.cgi?btOK=submit&i_mt_dirx={x}&i_mt_diry={y}&i_mt_dirz={z}',
            auth=HTTPDigestAuth(self.device.cgi_id, self.device.cgi_pw)
        )
        if resp.status_code != 200:
            raise TaskError(resp)
    except TaskError as e:
        raise e


@app.task(name='cam_task.offset_task', base=M2Task, bind=True)
def offset_task(self, did, x, y, z) -> dict:
    try:
        self.did = did
        resp = requests.get(
            f'http://{self.device.ip}/isp/appispmu.cgi?btOK=submit&i_mt_incx={x}&i_mt_incy={y}&i_mt_incz={z}',
            auth=HTTPDigestAuth(self.device.cgi_id, self.device.cgi_pw)
        )
        if resp.status_code != 200:
            raise TaskError(resp)
    except TaskError as e:
        raise e


@app.task(name='cam_task.test_callback')
def test_callback(*args, **kwargs):
    logger.info('Test callback')
    logger.info(f'args: {args}')
    logger.info(f'kwargs: {kwargs}')
    return args


@app.task(name='cam_task.test4', )
def test4(*args, **kwargs):
    logger.info(f'args: {args}')
    logger.info(f'kwargs: {kwargs}')
    group_tasks = [app.signature(f'cam_task.test{i + 1}') for i in range(3)]
    async_result = chain(
        group(group_tasks), test_callback.s()
    ).apply_async()
    logger.info(async_result)
