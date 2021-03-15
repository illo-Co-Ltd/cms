from flask import request, current_app, Blueprint
from flask_restplus import Resource

from .util.dto import UserDTO
from service.auth_service import *

jwt = current_app.extensions['flask-jwt-extended']
api = UserDTO.api
bp = Blueprint('auth', __name__, url_prefix='/auth')
_user = UserDTO.user


@jwt.user_identity_loader
def user_identity_lookup(user):
    if user:
        return user.id
    else:
        return None


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


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
@jwt_required(optional=True)
def login():
    data = request.get_json()
    return login_user(data)


@bp.route('/logout', methods=['POST'])
def logout():
    resp = {
        'msg': 'Logout successful.'
    }
    unset_jwt_cookies(resp)
    return resp


'''
@api.after_request
def refresh_expiring_jwts(resp):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        new_exp = datetime.timestamp(now + timedelta(minutes=30))
        if new_exp > exp_timestamp:
            access_token = create_access_token(identity=current_user)
            set_access_cookies(resp, access_token)
        return resp
    except (RuntimeError, KeyError):
        return resp
'''
