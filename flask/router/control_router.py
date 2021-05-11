from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from service.control_service import *

from router.dto.control_dto import *
from tasks import cam_task

api = api_control


@api.route('/capture')
class Capture(Resource):
    @api.doc('Capture')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(CaptureDTO.model, validate=True)
    @jwt_required()
    def post(self):
        try:
            return capture()
        except Exception as e:
            api.abort(400, message='Failed to capture', reason=e)


@api.route('/timelapse')
class Timelapse(Resource):
    @api.doc('Create timelapse task')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(TimelapseDTO.model, validate=True)
    @jwt_required()
    def post(self):
        try:
            return timelapse_start()
        except Exception as e:
            api.abort(400, message='Failed to start timelapse', reason=e)

    @api.doc('Delete timelapse task', params={'key': 'key of a task'})
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @jwt_required()
    def delete(self):
        data = request.get_json()
        key = data.get('key')
        if cam_task.stop_timelapse_send(key):
            return {'message': f'Timelapse task for key {key} deleted'}, 200
        else:
            api.abort(400, message=f'Cannot delete Timelapse task for key {key}')


@api.route('/range')
class Range(Resource):
    @api.doc('Get camera min/max range of position')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @jwt_required()
    def get(self):
        try:
            return get_position_range()
        except Exception as e:
            api.abort(400, message='Bad request', reason=e)


@api.route('/pos')
class Position(Resource):
    @api.doc('Offset camera position')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(PositionDTO.model)
    @jwt_required()
    def put(self):
        try:
            return offset_position()
        except Exception as e:
            api.abort(e.status_code, reason=e)

    @api.doc('Update camera position')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(PositionDTO.model)
    @jwt_required()
    # /pos?x=n&y=n&z=n
    def post(self):
        try:
            return set_position()
        except Exception as e:
            api.abort(e.status_code, reason=e)


# /focus?value=n
@api.route('/focus')
class Focus(Resource):
    @api.doc('Update camera focus')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @jwt_required()
    def put(self):
        try:
            return set_focus()
        except Exception as e:
            api.abort(e.status_code, reason=e)
