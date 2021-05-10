import os
import requests
from requests.auth import HTTPDigestAuth
import traceback

from flask import jsonify, request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from router.dto.control_dto import *
from tasks import cam_task
from model.db_base import db
from model.cell_model import Cell
from model.project_model import Project
from model.device_model import Device
from util.logger import logger

api = api_control
DEVICE_IP = os.environ.get('DEVICE_IP')
DEVICE_ID = os.environ.get('DEVICE_ID')
DEVICE_PW = os.environ.get('DEVICE_PW')


@api.route('/capture')
class Capture(Resource):
    @api.doc('Capture')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(CaptureDTO.model, validate=True)
    @jwt_required()
    def post(self):
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
            return jsonify(task_id), 200
        # TODO
        # 각 DB exception 에 따라 예외처리 세분화
        except Exception as e:
            logger.error(e)
            traceback.print_stack()
            traceback.print_exc()
            return jsonify({'message': 'Failed to capture'}), 400


@api.route('/timelapse')
class Timelapse(Resource):
    @api.doc('Create timelapse task')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(TimelapseDTO.model, validate=True)
    @jwt_required()
    def post(self):
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

    @api.doc('Delete timelapse task', params={'key':'key of a task'})
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @jwt_required()
    def delete(self):
        data = request.get_json()
        key = data.get('key')
        if cam_task.stop_timelapse_send(key):
            return jsonify({'message': f'Timelapse task for key {key} deleted'}), 200
        else:
            return jsonify({'message': f'Cannot delete Timelapse task for key {key}'}), 400


@api.route('/range')
class Range(Resource):
    @api.doc('Get camera min/max range of position')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @jwt_required()
    def get(self):
        logger.info('Fetch camera min/max range')


@api.route('/pos')
class Position(Resource):
    @api.doc('Offset camera position')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(PositionDTO.model)
    @jwt_required()
    def post(self):
        logger.info('Update relative camera position')
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
            return jsonify({
                'message': 'Successfully updated camera position.',
                'result': {"x": x, "y": y, "z": z}
            }), 200
        else:
            return jsonify({
                'message': 'Something went wrong'
            }), resp.status_code

    @api.doc('Update camera position')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(PositionDTO.model)
    @jwt_required()
    # /pos?x=n&y=n&z=n
    def put(self):
        logger.info('Update absolute camera position')
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
            return jsonify({
                'message': 'Successfully updated camera position.',
                'result': {"x": x, "y": y, "z": z}
            }), 200
        else:
            return jsonify({
                'message': 'Something went wrong'
            }), resp.status_code


# /focus?value=n
@api.route('/focus')
class Focus(Resource):
    @api.doc('Update camera focus')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @jwt_required()
    def put(self):
        logger.info('Update camera focus')
        data = request.get_json()
        newfocus = data.get('value')
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
                'message': 'Something went wrong'
            }), resp.status_code


# for test
def repeat(x, y, delay):
    import time
    for i in range(10):
        requests.get(
            f'http://{DEVICE_IP}/isp/appispmu.cgi?btOK=submit&i_mt_incx={x}&i_mt_incy={y}&i_mt_incz=0',
            auth=HTTPDigestAuth(DEVICE_ID, DEVICE_PW)
        )
        time.sleep(float(delay))
    return jsonify({'message': 'Success', }), 200
