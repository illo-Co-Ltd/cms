from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound

from router.data.data_dto import DeviceEntryDTO
from service.data.device_entry_service import create_device_entry, read_device_entry

api = DeviceEntryDTO.api
_device_entry = DeviceEntryDTO.device_entry


@api.route('/device_entry')
class DeviceEntry(Resource):
    @api.doc('Query device_entry with filters')
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(_device_entry, envelope='data')
    @jwt_required()
    def get(self):
        try:
            result = read_device_entry({
                'serial': request.args.get('serial'),
                'project': request.args.get('project'),
            })
            return result
        except Exception:
            api.abort(404)

    @api.doc('Create new device_entry')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.expect(_device_entry, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_device_entry(data)
        except NoResultFound:
            api.abort(400, message=f'Cannot find <{data.get("company")}> or <{data.get("owner")}>.')
        except Exception:
            api.abort(500, message='Failed to register device_entry')
