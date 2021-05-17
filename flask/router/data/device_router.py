from flask import request
from flask_restplus import Resource, reqparse, inputs
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from router.dto.data_dto import DeviceDTO
from service.data.device_service import *

api = DeviceDTO.api
DeviceDTO.model

parser_get = reqparse.RequestParser()
parser_get.add_argument('model', type=str, location='args')
parser_get.add_argument('serial', type=str, location='args')
parser_get.add_argument('company', type=str, location='args')
parser_get.add_argument('owner', type=str, location='args')
parser_get.add_argument('ip', type=str, location='args')
parser_get.add_argument('cgi_id', type=str, location='args')
parser_get.add_argument('cgi_pw', type=str, location='args')

parser_delete = reqparse.RequestParser()
parser_delete.add_argument('serial', type=str, location='args', required=True)


@api.route('/device')
class Device(Resource):
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(DeviceDTO.model, envelope='data')
    @api.expect(parser_get, validate=True)
    @jwt_required()
    def get(self):
        try:
            result = read_device(**parser_get.parse_args())
            return result
        except NoResultFound as e:
            api.abort(404, message=f'Cannot find device.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))

    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.expect(DeviceDTO.model, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_device(**data)
        except IntegrityError as e:
            api.abort(400, message=f'Need cgi_id field', reason=str(type(e)))
        except ValueError as e:
            api.abort(400, message=f'Need cgi_pw field', reason=str(type(e)))
        except NoResultFound as e:
            api.abort(400, message=f'Cannot find <{data.get("company")}> or <{data.get("owner")}>.',
                      reason=str(type(e)))
        except Exception as e:
            api.abort(500, message='Something went wrong.', reason=str(type(e)))

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(DeviceDTO.model_update, validate=False)
    @jwt_required()
    def put(self):
        data = request.get_json()
        try:
            return update_device(**data)
        except NoResultFound as e:
            api.abort(400, message=f'Cannot find device<{data.get("serial")}>.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message='Something went wrong.')

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(parser_delete)
    @jwt_required()
    def delete(self):
        try:
            args = parser_delete.parse_args()
            return delete_device(**args)
        except NoResultFound as e:
            api.abort(400, message=f'Cannot find device<{args.get("serial")}>.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message='Something went wrong.', reason=str(type(e)))
