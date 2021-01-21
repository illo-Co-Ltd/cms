import os
import requests
from flask import Blueprint, jsonify, request

from tasks import cv_task
from util.logger import logger

camera_route = Blueprint('camera_route', __name__)
DEVICE_IP = os.environ.get('DEVICE_IP')


@camera_route.route('/capture', methods=['GET'])
def img_capture():
    logger.info('Capture with camera')
    task_id = cv_task.capture('test')
    return jsonify(task_id)


@camera_route.route('/timelapse', methods=['POST'])
def img_timelapse():
    logger.info('Start timelapse')
    try:
        data = request.get_json()
        project = data.get('project')
        target = data.get('target')
        device = data.get('device')
        label = data.get('label')

    #        return jsonify(image.to_dict()), 200
    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Fail to create image metadata'}), 200


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
