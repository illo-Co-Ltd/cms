from flask import request, send_file
from flask_restplus import Resource, reqparse
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import BadRequest, HTTPException

from router.dto.data_dto import ImageMetadataDTO
from service.data.image_service import *

api = ImageMetadataDTO.api
_image_metadata = ImageMetadataDTO.model

parser_path = reqparse.RequestParser()
parser_path.add_argument('path', type=str, location='args', required=True)

# TODO
# created 시간 쿼리 가능하게 수정
parser_metadata = reqparse.RequestParser()
parser_metadata.add_argument('cell', type=str, location='args', required=False)
parser_metadata.add_argument('path', type=str, location='args', required=False)
parser_metadata.add_argument('device', type=str, location='args', required=False)
parser_metadata.add_argument('created', type=str, location='args', required=False)
parser_metadata.add_argument('created_by', type=str, location='args', required=False)
parser_metadata.add_argument('label', type=str, location='args', required=False)


@api.route('/image')
class Image(Resource):
    @api.response(404, 'No result found for query.')
    @api.produces(['image/jpg', 'image/png'])
    @api.expect(parser_path)
    @jwt_required()
    def get(self):
        try:
            return read_image(parser_path.parse_args().get('path'))
        except HTTPException as e:
            api.abort(e.code, message='Need a path field in query string', reason=str(type(e)))
        except FileNotFoundError as e:
            api.abort(404, message=f'Cannot find image.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))

    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.response(404, 'No result found for query.')
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_image(data)
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except NoResultFound:
            api.abort(404, message=f'Cannot find result for keys.')
        except Exception:
            api.abort(500, message='Failed to register image')

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.response(404, 'No result found for query.')
    @api.expect(parser_path)
    @jwt_required()
    def delete(self):
        try:
            args = parser_path.parse_args()
            return delete_image(**args)
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except NoResultFound as e:
            api.abort(404, message=f'Cannot find image<{args.get("path")}>.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message='Something went wrong.', reason=str(type(e)))


@api.route('/image/metadata')
class ImageMetadata(Resource):
    @api.response(404, 'No result found for query.')
    @api.marshal_list_with(_image_metadata, envelope='data')
    @api.expect(parser_metadata)
    @jwt_required()
    def get(self):
        try:
            return read_image_metadata(**parser_metadata.parse_args())
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except NoResultFound:
            api.abort(404, message=f'Cannot find result for filters.')
        except Exception:
            api.abort(500, message='Failed to read metadata')


    @api.response(201, 'Created')
    @api.response(404, 'No result found for query.')
    @api.expect(_image_metadata, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            return create_image_metadata(**data)
        except HTTPException as e:
            api.abort(e.code, message=e.description, reason=str(type(e)))
        except NoResultFound:
            api.abort(404, message=f'Cannot find result for keys.')
        except Exception:
            api.abort(500, message='Failed to register image')
