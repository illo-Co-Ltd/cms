from flask import request
from flask_restplus import Resource, reqparse
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import HTTPException

from router.dto.data_dto import DeviceEntryDTO
from service.data.device_entry_service import *

api = DeviceEntryDTO.api

parser = reqparse.RequestParser()
parser.add_argument('serial', type=str, location='args', required=False)
parser.add_argument('project', type=str, location='args', required=False)


@api.route('/device_entry')
class DeviceEntry(Resource):
    @api.doc('Query device_entry with filters')
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(DeviceEntryDTO.model, envelope='data')
    @api.expect(parser)
    @jwt_required()
    def get(self):
        try:
            result = read_device_entry(**parser.parse_args())
            return result
        except NoResultFound as e:
            api.abort(404, message=f'Cannot find device entry.', reason=str(type(e)))
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))

    @api.doc('Create new device_entry')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.expect(DeviceEntryDTO.model, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_device_entry(**data)
        except NoResultFound as e:
            api.abort(400, message=f'Cannot find <{data.get("serial") or data.get("project")}>.',
                      reason=str(type(e)))
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(parser)
    @jwt_required()
    def delete(self):
        try:
            args = parser.parse_args()
            return delete_device_entry(**args)
        except NoResultFound as e:
            api.abort(400, message=f'Cannot find with <{args.get("serial") or args.get("project")}>.',
                      reason=str(type(e)))
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except Exception as e:
            api.abort(500, message='Something went wrong.', reason=str(type(e)))
