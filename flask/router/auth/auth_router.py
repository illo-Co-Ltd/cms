from flask import request
from flask_restplus import Namespace, Resource
from flask_jwt_extended import jwt_required, current_user

from router.auth.jwt import unset_jwt
from router.data.data_dto import UserDTO
from service.auth_service import *

api = Namespace('auth', description='Authentication API')
_user = UserDTO.user


@api.route('/login')
class Login(Resource):
    @api.doc('Login')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    def post(self):
        data = request.get_json()
        return login_user(data)


@api.route('/logout')
class Logout(Resource):
    @api.doc('Logout')
    @api.response(200, 'OK')
    def get(self):
        resp = {
            'msg': 'Logout successful.'
        }
        return unset_jwt(resp)


@api.route('/whoami')
class WhoAmI(Resource):
    @api.doc('Return current user')
    @api.marshal_with(_user, mask='userid,username,company')
    @api.response(200, 'OK')
    @jwt_required()
    def get(self):
        resp = current_user
        return resp
