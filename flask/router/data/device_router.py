from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound

from router.data.data_dto import DeviceDTO
from service.data.device_service import create_device, read_device

api = DeviceDTO.api
_device = DeviceDTO.device


@api.route('/device')
class Device(Resource):
    @api.doc('Query device with filters')
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(_device, envelope='data')
    @jwt_required()
    def get(self):
        try:
            result = read_device({
                'model': request.args.get('model'),
                'serial': request.args.get('serial'),
                'company': request.args.get('company'),
                'owner': request.args.get('owner'),
                'ip': request.args.get('ip'),
            })
            return result
        except Exception:
            api.abort(404)

    @api.doc('Create new device')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.expect(_device, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_device(data)
        except NoResultFound:
            api.abort(400, message=f'Cannot find <{data.get("company")}> or <{data.get("owner")}>.')
        except Exception:
            api.abort(500, message='Failed to register device')
