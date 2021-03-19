from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound

from ..util.dto import DeviceEntryDTO
from service.device_entry_service import *
from util.logger import logger

api = DeviceEntryDTO.api
_device_entry = DeviceEntryDTO.device_entry


@api.route('')
class DeviceEntry(Resource):
    @api.doc('query device_entry with filters')
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(_device_entry, envelope='data')
    @jwt_required()
    def get(self):
        try:
            result = read_device_entry({
                'serial': request.args.get('serial'),
                'project': request.args.get('project'),
            })
            logger.info(result)
            return result
        except Exception:
            api.abort(404)

    @api.doc('query device_entry with filters')
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
