import traceback
from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from router.dto.data_dto import UserDTO
from service.data.user_service import create_user, read_user
from util.logger import logger

api = UserDTO.api
_user = UserDTO.model


@api.route('/user')
class User(Resource):
    @api.doc('Get current user info')
    @api.marshal_with(_user, mask='userid,username,company')
    @jwt_required()
    def get(self):
        try:
            resp = read_user({
                'userid': request.args.get('userid'),
                'username': request.args.get('username'),
                'company': request.args.get('company')
            })
            logger.info(request.args)
            return resp
        except Exception:
            logger.error('Cannot read user')
            logger.debug(traceback.format_exc())
            api.abort(404)

    @api.doc('Register new user')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.response(409, 'Resource already exists')
    @api.expect(_user, validate=True)
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            resp = create_user(data)
            return resp
        except Exception as e:
            api.abort(reason=e)
