from flask import make_response
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import HTTPException

from service.control_service import *

from router.dto.control_dto import *
from worker import cam_task

api = api_control


@api.route('/jpeg/<serial>')
class Jpeg(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.produces(['image/jpeg'])
    @jwt_required()
    def get(self, serial):
        try:
            img = fetch_jpeg(serial)
            resp = make_response(img)
            resp.headers.set('Content-Type', 'image/jpeg')
            return resp
        except NoResultFound as e:
            api.abort(404, message=f'Cannot find device.', reason=str(type(e)))
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))


@api.route('/capture')
class Capture(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(CaptureDTO.model, validate=True)
    @jwt_required()
    def post(self):
        try:
            return capture(**(request.get_json()))
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))


@api.route('/timelapse')
class Timelapse(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(TimelapseDTO.model, validate=True)
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            return timelapse_start(**data)
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @jwt_required()
    def delete(self):
        try:
            data = request.get_json()
            key = data.get('key')
            if cam_task.send_stop_timelapse(key):
                return {'message': f'Timelapse task for key {key} deleted'}, 200
            else:
                raise Exception('cannot stop timelapse')
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))


@api.route('/range')
class Range(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @jwt_required()
    def get(self):
        try:
            return get_position_range()
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))


@api.route('/pos')
class Position(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(PositionDTO.model)
    @jwt_required()
    def put(self):
        try:
            data = request.get_json()
            return offset_position(**data)
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(PositionDTO.model)
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            return set_position(**data)
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))


@api.route('/focus')
class Focus(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(FocusDTO.model)
    @jwt_required()
    def put(self):
        try:
            data = request.get_json()
            return set_focus(**data)
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))


@api.route('/led')
class Led(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(LedDTO.model)
    @jwt_required()
    def put(self):
        try:
            data = request.get_json()
            return set_led(**data)
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))
