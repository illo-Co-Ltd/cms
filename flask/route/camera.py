import os
import requests
from requests.auth import HTTPDigestAuth
import traceback

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from tasks import cam_task
from model.db_base import db
from model.target_model import Target
from model.project_model import Project
from model.device_model import Device
from util.logger import logger

camera_route = Blueprint('camera_route', __name__)
DEVICE_IP = os.environ.get('DEVICE_IP')
DEVICE_ID = os.environ.get('DEVICE_ID')
DEVICE_PW = os.environ.get('DEVICE_PW')


@camera_route.route('/capture', methods=['POST'])
@jwt_required()
def capture():
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
            task_id = cam_task.capture_send(header=f'{pid.shorthand}_{tid.name}',
                                            data={'target': tid.id,
                                                  'device': did.id,
                                                  'label': label})
        else:
            task_id = cam_task.capture_send(header=f'{project}_{target}',
                                            data={'target': None,
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


@camera_route.route('/timelapse/start', methods=['POST'])
@jwt_required()
def start_timelapse():
    logger.info('Start timelapse')
    try:
        data = request.get_json()
        project = data.get('project')
        target = data.get('target')
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
                    'target': None,
                    'device': None,
                    'label': None
                }
            }
        else:
            pid = db.session.query(Project).filter_by(name=project).one()
            tid = db.session.query(Target) \
                .filter_by(project=pid.id) \
                .filter_by(name=target).one()
            did = db.session.query(Device).filter_by(serial=device).one()
            kwargs = {
                'header': pid.shorthand,
                'run_every': run_every,
                'expire_at': expire_at,
                'data': {
                    'target': tid.id,
                    'device': did.id,
                    'label': label
                }
            }
        logger.info(kwargs)
        status, key = cam_task.start_timelapse_send(**kwargs)
        if status:
            return jsonify({
                'message': f'Timelapse task for device {kwargs.get("data").get("device")} queued',
                'key': key
            }), 200
        else:
            raise Exception('Result false')
    except Exception as e:
        # TODO
        # 각 DB exception 에 따라 예외처리 세분화
        traceback.print_stack()
        traceback.print_exc()
        logger.error(e)
        return jsonify({'message': 'Failed to start timelapse'}), 200


@camera_route.route('/timelapse/stop', methods=['POST'])
@jwt_required()
def stop_timelapse():
    data = request.get_json()
    key = data.get('key')
    if cam_task.stop_timelapse_send(key):
        return jsonify({'message': f'Timelapse task for key {key} deleted'}), 200
    else:
        return jsonify({'message': f'Cannot delete Timelapse task for key {key}'}), 200


@camera_route.route('/range', methods=['GET'])
@jwt_required()
def get_position_range():
    logger.info('Fetch camera min/max range')


# /pos?x=n&y=n&z=n
@camera_route.route('/pos', methods=['GET'])
@jwt_required()
def update_position():
    logger.info('Update absolute camera position')
    x = request.args.get('x')
    y = request.args.get('y')
    z = request.args.get('z')

    logger.info('newpos: ', {"x": x, "y": y, "z": z})
    resp = requests.get(
        f'http://{DEVICE_IP}/isp/appispmu.cgi?btOK=submit&i_mt_dirx={x}&i_mt_diry={y}&i_mt_dirz={z}',
        auth=HTTPDigestAuth(DEVICE_ID, DEVICE_PW)
    )
    # logger.info(resp.text)
    if resp.status_code == 200:
        return jsonify({
            'message': 'Successfully updated camera position.',
            'result': {"x": x, "y": y, "z": z}
        }), 200
    else:
        return jsonify({
            'message': 'Cannot connect to device'
        }), 404


# /pos_offset?x=n&y=n&z=n
@camera_route.route('/pos_offset', methods=['GET'])
@jwt_required()
def offset_position():
    logger.info('Update relative camera position')
    x = request.args.get('x')
    y = request.args.get('y')
    z = request.args.get('z')

    logger.info('offset: ' + str({"x": x, "y": y, "z": z}))
    resp = requests.get(
        f'http://{DEVICE_IP}/isp/appispmu.cgi?btOK=submit&i_mt_incx={x}&i_mt_incy={y}&i_mt_incz={z}',
        auth=HTTPDigestAuth(DEVICE_ID, DEVICE_PW)
    )
    logger.info(resp.text)
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
@jwt_required()
def update_focus():
    logger.info('Update camera focus')
    newfocus = request.args.get('value')
    logger.info(f'newfocus: {newfocus}')
    resp = requests.get(
        f'http://{DEVICE_IP}/isp/appispmu.cgi?i_c1_dirfcs={newfocus}&btOK=move',
        auth=HTTPDigestAuth(DEVICE_ID, DEVICE_PW)
    )
    if resp.status_code == 200:
        return jsonify({
            'message': 'Successfully updated camera focus.',
            'result': newfocus
        }), 200
    else:
        return jsonify({
            'message': 'Cannot connect to device'
        }), 404


# for test
@camera_route.route('/repeat/<x>/<y>/<delay>', methods=['GET'])
@jwt_required()
def repeat(x, y, delay):
    import time
    for i in range(10):
        requests.get(
            f'http://{DEVICE_IP}/isp/appispmu.cgi?btOK=submit&i_mt_incx={x}&i_mt_incy={y}&i_mt_incz=0',
            auth=HTTPDigestAuth(DEVICE_ID, DEVICE_PW)
        )
        time.sleep(float(delay))
    return jsonify({'message': 'Success', }), 200
