import os
import traceback

import requests
from flask import request
from requests.auth import HTTPDigestAuth

from model.db_base import db
from model import Project, Cell, Device
from tasks import cam_task
from util.logger import logger
from util.exc import CGIException

DEVICE_IP = os.environ.get('DEVICE_IP')
DEVICE_ID = os.environ.get('DEVICE_ID')
DEVICE_PW = os.environ.get('DEVICE_PW')


def capture():
    logger.info('Capture with camera')
    try:
        data = request.get_json()
        project = data.get('project')
        cell = data.get('cell')
        device = data.get('device')
        label = data.get('label')
        debug = data.get('debug')

        # skip integrity check if debugging
        if not debug:
            pid = db.session.query(Project).filter_by(name=project).one()
            tid = db.session.query(Cell) \
                .filter_by(project=pid.id) \
                .filter_by(name=cell).one()
            did = db.session.query(Device).filter_by(serial=device).one()
            task_id = cam_task.capture_send(header=f'{pid.shorthand}_{tid.name}',
                                            data={'cell': tid.id,
                                                  'device': did.id,
                                                  'label': label})
        else:
            task_id = cam_task.capture_send(header=f'{project}_{cell}',
                                            data={'cell': None,
                                                  'device': None,
                                                  'label': None})
        return task_id, 200
    # TODO
    # 각 DB exception 에 따라 예외처리 세분화
    except Exception as e:
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()
        raise e


def timelapse_start():
    logger.info('Start timelapse')
    try:
        data = request.get_json()
        project = data.get('project')
        cell = data.get('cell')
        device = data.get('device')
        label = data.get('label')
        run_every = data.get('run_every')
        expire_at = data.get('expire_at')
        debug = data.get('debug')

        # skip integrity check if debugging
        if debug:
            kwargs = {
                'header': 'test',
                'run_every': run_every,
                'expire_at': None,
                'data': {
                    'cell': None,
                    'device': None,
                    'label': None
                }
            }
        else:
            pid = db.session.query(Project).filter_by(name=project).one()
            tid = db.session.query(Cell) \
                .filter_by(project=pid.id) \
                .filter_by(name=cell).one()
            did = db.session.query(Device).filter_by(serial=device).one()
            kwargs = {
                'header': pid.shorthand,
                'run_every': run_every,
                'expire_at': expire_at,
                'data': {
                    'cell': tid.id,
                    'device': did.id,
                    'label': label
                }
            }
        logger.info(kwargs)
        status, key = cam_task.send_start_timelapse(**kwargs)
        if status:
            return {
                       'message': f'Timelapse task for device {kwargs.get("data").get("device")} queued',
                       'key': key
                   }, 200
        else:
            raise Exception('Result false')
    except Exception as e:
        # TODO
        # 각 DB exception 에 따라 예외처리 세분화
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()
        raise e


def get_position_range():
    logger.info('Fetch camera min/max range')
    pass


def set_position():
    logger.info('Update absolute camera position')
    try:
        data = request.get_json()
        x = data.get('x')
        y = data.get('y')
        z = data.get('z')
        logger.info('newpos: ', {"x": x, "y": y, "z": z})
        resp = requests.get(
            f'http://{DEVICE_IP}/isp/appispmu.cgi?btOK=submit&i_mt_dirx={x}&i_mt_diry={y}&i_mt_dirz={z}',
            auth=HTTPDigestAuth(DEVICE_ID, DEVICE_PW)
        )
        # logger.info(resp.text)
        if resp.status_code == 200:
            return {
                       'message': 'Successfully updated camera position.',
                       'result': {"x": x, "y": y, "z": z}
                   }, 200
        else:
            raise CGIException(resp)
    except Exception as e:
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()
        raise e


def offset_position():
    logger.info('Update relative camera position')
    try:
        data = request.get_json()
        x = data.get('x')
        y = data.get('y')
        z = data.get('z')

        logger.info('offset: ' + str({"x": x, "y": y, "z": z}))
        resp = requests.get(
            f'http://{DEVICE_IP}/isp/appispmu.cgi?btOK=submit&i_mt_incx={x}&i_mt_incy={y}&i_mt_incz={z}',
            auth=HTTPDigestAuth(DEVICE_ID, DEVICE_PW)
        )
        logger.info(resp.text)
        if resp.status_code == 200:
            return {
                       'message': 'Successfully updated camera position.',
                       'result': {"x": x, "y": y, "z": z}
                   }, 200
        else:
            raise CGIException(resp)
    except Exception as e:
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()
        raise e


def set_focus():
    logger.info('Update camera focus')
    try:
        data = request.get_json()
        newfocus = data.get('value')
        logger.info(f'newfocus: {newfocus}')
        resp = requests.get(
            f'http://{DEVICE_IP}/isp/appispmu.cgi?i_c1_dirfcs={newfocus}&btOK=move',
            auth=HTTPDigestAuth(DEVICE_ID, DEVICE_PW)
        )
        if resp.status_code == 200:
            return {
                       'message': 'Successfully updated camera focus.',
                       'result': newfocus
                   }, 200
        else:
            raise CGIException(resp)
    except Exception as e:
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()
        raise e
