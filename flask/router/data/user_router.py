import traceback
from flask import request
from flask_restplus import Resource, reqparse
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from router.dto.data_dto import UserDTO
from service.data.user_service import *
from util.logger import logger

api = UserDTO.api
_user = UserDTO.model

parser_get = reqparse.RequestParser()
parser_get.add_argument('userid', type=str, location='args')
parser_get.add_argument('username', type=str, location='args')
parser_get.add_argument('company', type=str, location='args')

parser_delete = reqparse.RequestParser()
parser_delete.add_argument('userid', type=str, location='args', required=True)


@api.route('/user')
class User(Resource):
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.response(404, 'Not found')
    @api.marshal_with(_user, mask='userid,username,company')
    @api.expect(parser_get)
    @jwt_required()
    def get(self):
        try:
            return read_user(**parser_get.parse_args())
        except NoResultFound as e:
            api.abort(404, message=f'Cannot find user.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))

    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.response(409, 'Resource already exists')
    @api.expect(_user, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            resp = create_user(**data)
            return resp
        except InvalidRequestError as e:
            api.abort(400, message=f'Field is unacceptable', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(UserDTO.model)
    @jwt_required()
    def put(self):
        try:
            data = request.get_json()
            return update_user(**data)
        except NotEnoughPermission as e:
            api.abort(403, message=f'Not enough permission.', reason=str(type(e)))
        except NoResultFound as e:
            api.abort(400, message=f'Cannot find user.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))

    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.response(403, 'Forbidden')
    @api.expect(parser_delete)
    @jwt_required()
    def delete(self):
        try:
            return delete_user(**parser_delete.parse_args())
        except NotEnoughPermission as e:
            api.abort(403, message=f'Not enough permission.', reason=str(type(e)))
        except NoResultFound as e:
            api.abort(404, message=f'Cannot find user.', reason=str(type(e)))
        except Exception as e:
            api.abort(500, message=f'Something went wrong.', reason=str(type(e)))
