from flask import request
from flask_restplus import Resource, reqparse, inputs
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.orm.exc import NoResultFound

from router.dto.data_dto import DeviceDTO
from service.data.device_service import *

api = DeviceDTO.api
_device = DeviceDTO.model

parser = reqparse.RequestParser()


# parser.add_argument('model', type=)

@api.route('/device')
class Device(Resource):
    @api.doc('Query device with filters')
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(_device, envelope='data')
    @api.expect(parser, validate=True)
    @jwt_required()
    def get(self):
        logger.info(get_jwt()["exp"])
        try:
            result = read_device(
                model=request.args.get('model'),
                serial=request.args.get('serial'),
                company=request.args.get('company'),
                owner=request.args.get('owner'),
                ip=request.args.get('ip')
            )
            return result
        except NoResultFound as e:
            api.abort(404, message=f'Cannot find device.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))

    @api.doc('Create new device')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.expect(_device, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_device(**data)
        except NoResultFound as e:
            api.abort(400, message=f'Cannot find <{data.get("company")}> or <{data.get("owner")}>.',
                      reason=str(type(e)))
        except Exception as e:
            api.abort(500, message='Something went wrong.', reason=str(type(e)))

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.doc(params={
        'serial': 'Key to find device (required)',
        'model': 'New model name',
        'newserial': 'New serial number',
        'company': 'New company name',
        'owner': 'New owner id',
        'ip': 'New shorthand',
    })
    @jwt_required()
    def put(self):
        data = request.get_json()
        try:
            return update_device(**data)
        except NoResultFound as e:
            api.abort(400, message=f'Cannot find device<{data.get("name")}>.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message='Something went wrong.')

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.doc(params={
        'serial': 'Key to find device (required)',
    })
    @jwt_required()
    def delete(self):
        data = request.get_json()
        try:
            return delete_device(**data)
        except NoResultFound as e:
            api.abort(400, message=f'Cannot find device<{data.get("name")}>.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message='Something went wrong.', reason=str(type(e)))
