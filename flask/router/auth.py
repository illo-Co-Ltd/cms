from flask import request, Blueprint
from flask_restplus import Resource

from .util.dto import UserDTO
from .util.jwt import unset_jwt
from service.auth_service import *

api = UserDTO.api
bp = Blueprint('auth', __name__, url_prefix='/auth')
_user = UserDTO.user


@api.route('')
class UserAuth(Resource):
    @api.doc('Get current user')
    @api.marshal_with(_user, mask='userid,username,company')
    @jwt_required()
    def get(self):
        resp = current_user
        return resp

    @api.doc('Register new user')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.response(409, 'Resource already exists')
    @api.expect(_user, validate=True)
    def post(self):
        data = request.get_json()
        try:
            resp = create_user(data)
            return resp
        except Exception as e:
            api.abort(500, reason=e)


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data)


@bp.route('/logout', methods=['POST'])
def logout():
    resp = {
        'msg': 'Logout successful.'
    }
    return unset_jwt(resp)


