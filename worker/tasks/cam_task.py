import os
import datetime, pytz
from contextlib import contextmanager
import traceback

import celery
import sqlalchemy
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
from .util import check_and_create
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
        ctime = datetime.datetime.now(pytz.timezone("Asia/Seoul"))
        with self.session_scope() as session:
            device = session.execute(
                text("SELECT * FROM device WHERE id=:device_id"),
                {'device_id':data.get('device')}
            ).fetchone()
        resp = requests.get(
            f'http://{device.ip}/jpg/',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code != 200:
            logger.error(resp.text)
            raise TaskError(resp)
        fname = f'{ctime.strftime("%Y-%m-%dT%H-%M-%S-%f")}.jpg'
        fpath = f'/data/{data.get("path")}/{fname}'
        check_and_create(os.path.dirname(fpath))

        img = cv2.imdecode(np.frombuffer(resp.content, dtype=np.uint8), -1)
        res = cv2.imwrite(fpath, img)
        if not res:
            raise TaskError('Nothing written by cv2')
        else:
            # save metadata to db
            with self.session_scope() as session:
                session.execute(
                    text(f'''INSERT INTO image('cell_id','path',)
                    ''')
                )
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
