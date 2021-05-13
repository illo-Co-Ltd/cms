from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from util.jwt import unset_jwt
from router.dto.auth_dto import *
from service.auth.auth_service import *

api = api_auth


@api.route('/login')
class Login(Resource):
    @api.doc('Login')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.expect(LoginDTO.model, validate=True)
    def post(self):
        data = request.get_json()
        return login_user(**data)


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
    @api.marshal_with(WhoAmIDTO.model)
    @api.response(200, 'OK')
    @jwt_required()
    def get(self):
        resp = current_user
        return resp
