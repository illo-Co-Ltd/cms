from flask import request
from flask_restplus import Namespace, Resource

from router.auth.jwt import unset_jwt
from service.auth_service import *

api = Namespace('auth', description='Authentication API')


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
