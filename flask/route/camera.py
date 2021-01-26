import os
import requests
import traceback
from flask import Blueprint, jsonify, request

from tasks import cv_task
from model.db_base import db
from model.target_model import Target
from model.project_model import Project
from model.device_model import Device
from util.logger import logger

camera_route = Blueprint('camera_route', __name__)
DEVICE_IP = os.environ.get('DEVICE_IP')


@camera_route.route('/capture', methods=['POST'])
def img_capture():
    logger.info('Capture with camera')
    try:
        data = request.get_json()
        project = data.get('project')
        target = data.get('target')
        device = data.get('device')
        label = data.get('label')
        debug = data.get('debug')

        # skip integrity check if debugging
        if not debug:
            pid = db.session.query(Project).filter_by(name=project).one()
            tid = db.session.query(Target) \
                .filter_by(project=pid.id) \
                .filter_by(name=target).one()
            did = db.session.query(Device).filter_by(serial=device).one()
            task_id = cv_task.capture(header=f'{pid.shorthand}_{tid.name}',
                                      params={'target': tid.id,
                                              'device': did.id,
                                              'label': label})
        else:
            task_id = cv_task.capture(header=f'{project}_{target}',
                                      params={'target': None,
                                              'device': None,
                                              'label': None})
        return jsonify(task_id)
    # TODO
    # 각 DB exception 에 따라 예외처리 세분화
    except Exception as e:
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()
        return jsonify({'message': 'Failed to capture'}), 200


@camera_route.route('/timelapse', methods=['POST'])
def img_timelapse():
    logger.info('Start timelapse')
    try:
        data = request.get_json()
        project = data.get('project')
        target = data.get('target')
        device = data.get('device')
        label = data.get('label')
        interval = data.get('interval')
        expire_at = data.get('expire_at')
        debug = data.get('debug')

        # skip integrity check if debugging
        if not debug:
            pid = db.session.query(Project).filter_by(name=project).one()
            tid = db.session.query(Target) \
                .filter_by(project=pid.id) \
                .filter_by(name=target).one()
            did = db.session.query(Device).filter_by(serial=device).one()

        cv_task.periodic_capture(
            header=pid.shorthand,
            run_every=interval,
            expire_at=expire_at,
            params={
                'target': tid.id,
                'device': did.id,
                'label': label
            }
        )
        return jsonify({'message': f'Timelapse task for device {did.serial} registered'}), 200
    except Exception as e:
        # TODO
        # 각 DB exception 에 따라 예외처리 세분화
        logger.error(e)
        traceback.print_stack()
        traceback.print_exc()
        return jsonify({'message': 'Failed to start timelapse'}), 200


@camera_route.route('/range', methods=['GET'])
def get_position_range():
    logger.info('Fetch camera min/max range')


# /pos?x=n&y=n&z=n
@camera_route.route('/pos', methods=['GET'])
def update_position():
    logger.info('Update camera position')
    x = request.args.get('x')
    y = request.args.get('y')
    z = request.args.get('z')

    logger.info(f'newpos: {"x":x,"y":y, "z":z}')
    resp = requests.get(f'http://{DEVICE_IP}/isp/appispmu.cgi?btOK=submit&i_mt_dirx={x}&i_mt_diry={y}&i_mt_dirz={z}')
    if resp.status_code == 200:
        return jsonify({
            'message': 'Successfully updated camera position.',
            'result': {"x": x, "y": y, "z": z}
        }), 200
    else:
        return jsonify({
            'message': 'Cannot connect to device'
        }), 404


# /focus?value=n
@camera_route.route('/focus', methods=['GET'])
def update_focus():
    logger.info('Update camera focus')
    newfocus = request.args.get('value')
    logger.info(f'newfocus: {newfocus}')
    resp = requests.get(f'http://{DEVICE_IP}/isp/appispmu.cgi?i_c1_dirfcs={newfocus}&btOK=move')
    if resp.status_code == 200:
        return jsonify({
            'message': 'Successfully updated camera focus.',
            'result': newfocus
        }), 200
    else:
        return jsonify({
            'message': 'Cannot connect to device'
        }), 404
