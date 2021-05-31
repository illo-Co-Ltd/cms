import os
import traceback

import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ETree
from flask_jwt_extended import get_jwt_identity
from flask import request

from model.db_base import db
from model import Project, Cell, Device
from worker import camera
from util.logger import logger
from util.exc import CGIException


def fetch_jpeg(serial):
    logger.info('Fetch jpeg image from camera')
    try:
        ip = db.session.query(Device).filter_by(serial=serial).one().ip
        device = db.session.query(Device).filter_by(serial=serial).one()
        resp = requests.get(
            f'http://{ip}/jpg/',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code == 200:
            return resp.content
        else:
            logger.error(resp.text)
            raise CGIException(resp)
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def capture(serial, project, cell, label, path):
    logger.info('Capture with camera')
    try:
        project = db.session.query(Project).filter_by(name=project).one()
        cell = db.session.query(Cell) \
            .filter_by(project=project) \
            .filter_by(name=cell).one()
        device = db.session.query(Device).filter_by(serial=serial).one()
        task_id = camera.send_capture(
            data={
                'project': project.id,
                'cell': cell.id,
                'device': device.id,
                'label': label,
                'path': path,
                'created_by_id': get_jwt_identity()
            }
        )
        return task_id, 200
    # TODO
    # 각 DB exception 에 따라 예외처리 세분화
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def timelapse_start(serial, project, cell, label, run_every, expire_at, debug):
    logger.info('Start timelapse')
    try:
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
            did = db.session.query(Device).filter_by(serial=serial).one()
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
        status, key = camera.send_start_timelapse(**kwargs)
        if status:
            return {
                       'message': f'Timelapse task for device {kwargs.get("data").get("serial")} queued',
                       'key': key
                   }, 200
        else:
            raise Exception('Result false')
    except Exception as e:
        # TODO
        # 각 DB exception 에 따라 예외처리 세분화
        db.session.rollback()
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def get_position_range(serial):
    logger.info('Get camera max position')
    try:
        device = db.session.query(Device).filter_by(serial=serial).one()
        cgi_d100 = f'http://{device.ip}/isp/st_d100.xml'
        resp = requests.get(
            cgi_d100,
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code != 200:
            raise CGIException(resp)
        resp.encoding = None
        tree = ETree.fromstring(resp.text)
        d100 = tree.find('D100')
        endx = d100.find('ENDX').text
        endy = d100.find('ENDY').text
        endz = d100.find('ENDZ').text
        return {'x': endx, 'y': endy, 'z': endz}
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def get_position(serial):
    logger.info('Get absolute camera position')
    try:
        device = db.session.query(Device).filter_by(serial=serial).one()
        cgi_d100 = f'http://{device.ip}/isp/st_d100.xml'
        resp = requests.get(
            cgi_d100,
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code != 200:
            raise CGIException(resp)
        resp.encoding = None
        tree = ETree.fromstring(resp.text)
        d100 = tree.find('D100')
        curx = d100.find('CURX').text
        cury = d100.find('CURY').text
        curz = d100.find('CURZ').text
        return {'x': curx, 'y': cury, 'z': curz}
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def set_position(serial, x, y, z):
    logger.info('Update absolute camera position')
    try:
        logger.info('newpos: ', {"x": x, "y": y, "z": z})
        device = db.session.query(Device).filter_by(serial=serial).one()
        resp = requests.get(
            f'http://{device.ip}/isp/appispmu.cgi?btOK=submit&i_mt_dirx={x}&i_mt_diry={y}&i_mt_dirz={z}',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
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
        logger.debug(traceback.format_exc())
        raise e


def offset_position(serial, x, y, z):
    logger.info('Update relative camera position')
    try:
        logger.info('offset: ' + str({"x": x, "y": y, "z": z}))
        device = db.session.query(Device).filter_by(serial=serial).one()
        resp = requests.get(
            f'http://{device.ip}/isp/appispmu.cgi?btOK=submit&i_mt_incx={x}&i_mt_incy={y}&i_mt_incz={z}',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
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
        logger.debug(traceback.format_exc())
        raise e


def get_delay(serial):
    logger.info('Get camera movement delay')
    try:
        device = db.session.query(Device).filter_by(serial=serial).one()
        cgi_d100 = f'http://{device.ip}/isp/st_d100.xml'
        resp = requests.get(
            cgi_d100,
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code != 200:
            raise CGIException(resp)
        resp.encoding = None
        tree = ETree.fromstring(resp.text)
        d100 = tree.find('D100')
        delay = d100.find('DLY').text
        return {'delay': delay}
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def set_delay(serial, delay):
    logger.info('Change movement delay')
    try:
        logger.info(f'delay: {delay}')
        device = db.session.query(Device).filter_by(serial=serial).one()
        resp = requests.get(
            f'http://{device.ip}/isp/appispmu.cgi?btOK=submit&i_mt_dly={delay}',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code == 200:
            return {
                       'message': 'Successfully updated delay.',
                       'result': delay
                   }, 200
        else:
            raise CGIException(resp)
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def autofocus(serial):
    logger.info('Auto adjust focus')
    try:
        device = db.session.query(Device).filter_by(serial=serial).one()
        resp = requests.get(
            f'http://{device.ip}/isp/appispmu.cgi?i_c1_dirafc=+run+',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code == 200:
            return {
                       'message': 'Successfully adjusted focus.',
                   }, 200
        else:
            raise CGIException(resp)
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def get_focus(serial):
    logger.info('Get camera focus')
    try:
        device = db.session.query(Device).filter_by(serial=serial).one()
        cgi_c100 = f'http://{device.ip}/isp/st_c100.xml'
        resp = requests.get(
            cgi_c100,
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code != 200:
            raise CGIException(resp)
        resp.encoding = None
        tree = ETree.fromstring(resp.text)
        c100 = tree.find('C100')
        focus = c100.find('CURFCS').text
        return {'focus': focus}
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def set_focus(serial, focus):
    logger.info('Update camera focus')
    try:
        logger.info(f'focus: {focus}')
        device = db.session.query(Device).filter_by(serial=serial).one()
        resp = requests.get(
            f'http://{device.ip}/isp/appispmu.cgi?i_c1_dirfcs={focus}&btOK=move',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code == 200:
            return {
                       'message': 'Successfully updated camera focus.',
                       'result': focus
                   }, 200
        else:
            raise CGIException(resp)
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def offset_focus(serial, focus):
    logger.info('Relatively update camera focus')
    logger.info(f'focus offset: {focus}')
    try:
        # Fetching current value
        device = db.session.query(Device).filter_by(serial=serial).one()
        cgi_c100 = f'http://{device.ip}/isp/st_c100.xml'
        resp = requests.get(
            cgi_c100,
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code != 200:
            raise CGIException(resp)
        resp.encoding = None
        tree = ETree.fromstring(resp.text)
        c100 = tree.find('C100')
        current = int(c100.find('CURFCS').text)
        target = current+focus
        if target<1:
            target=1
        if target>255:
            target=255
        # update
        resp = requests.get(
            f'http://{device.ip}/isp/appispmu.cgi?i_c1_dirfcs={str(target)}&btOK=move',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code == 200:
            return {
                       'message': 'Successfully updated camera focus.',
                       'result': target
                   }, 200
        else:
            raise CGIException(resp)
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def get_led(serial):
    logger.info('Get led brightness')
    try:
        device = db.session.query(Device).filter_by(serial=serial).one()
        cgi_c100 = f'http://{device.ip}/isp/st_c100.xml'
        resp = requests.get(
            cgi_c100,
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code != 200:
            raise CGIException(resp)
        resp.encoding = None
        tree = ETree.fromstring(resp.text)
        c100 = tree.find('C100')
        led = c100.find('CURLED').text
        return {'led': led}
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def set_led(serial, led):
    logger.info('Update led brightness')
    try:
        logger.info(f'led: {led}')
        device = db.session.query(Device).filter_by(serial=serial).one()
        resp = requests.get(
            f'http://{device.ip}/isp/appispmu.cgi?i_c1_dirled={led}&btOK=run',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code == 200:
            return {
                       'message': 'Successfully updated led brightness.',
                       'result': led
                   }, 200
        else:
            raise CGIException(resp)
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e


def stop(serial):
    logger.info('Stop moving position')
    try:
        device = db.session.query(Device).filter_by(serial=serial).one()
        resp = requests.get(
            f'http://{device.ip}/isp/appispmu.cgi?i_mt_stop=submit',
            auth=HTTPDigestAuth(device.cgi_id, device.cgi_pw)
        )
        if resp.status_code == 200:
            return {
                       'message': 'Successfully stopped movement.',
                   }, 200
        else:
            raise CGIException(resp)
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e
