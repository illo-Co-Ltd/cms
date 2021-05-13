from datetime import datetime, timezone, timedelta
from functools import wraps

from flask import make_response, current_app
from flask_jwt_extended import unset_jwt_cookies, verify_jwt_in_request, get_jwt, create_access_token, current_user, set_access_cookies

from model.model_import import User

jwt = current_app.extensions['flask-jwt-extended']


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


def unset_jwt(resp):
    resp = make_response(resp)
    unset_jwt_cookies(resp)
    return resp


def refresh_token(resp):
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