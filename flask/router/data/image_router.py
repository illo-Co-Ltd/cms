from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound

from router.data.data_dto import ImageDTO
from service.data.image_service import create_image, read_image

api = ImageDTO.api
_image = ImageDTO.image


@api.route('/image')
class Image(Resource):
    @api.doc('Query image with filters')
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(_image, envelope='data')
    @jwt_required()
    def get(self):
        try:
            result = read_image({
                'cell': request.args.get('cell'),
                'path': request.args.get('path'),
                'device': request.args.get('device'),
                'created': request.args.get('created'),
                'created_by': request.args.get('created_by'),
                'label': request.args.get('label'),
                'offset_x': request.args.get('offset_x'),
                'offset_y': request.args.get('offset_y'),
                'offset_z': request.args.get('offset_z'),
                'pos_x': request.args.get('pos_x'),
                'pos_y': request.args.get('pos_y'),
                'pos_z': request.args.get('pos_z'),
            })
            return result
        except Exception:
            api.abort(404)

    @api.doc('Create new image')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.expect(_image, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_image(data)
        except NoResultFound:
            api.abort(400, message=f'Cannot find result for keys.')
        except Exception:
            api.abort(500, message='Failed to register image')
