import os
import traceback
from datetime import datetime, timezone, timedelta

from flask import after_this_request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    get_jwt, current_user

from model.model_import import User
from util.logger import logger

app = current_app

JWT_EXPR = app.config['JWT_ACCESS_TOKEN_EXPIRES']


def _set_cookies(access_token, refresh_token):
    @after_this_request
    def _internal(response):
        set_access_cookies(response, access_token)
        # set_refresh_cookies(response, refresh_token)
        return response


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + JWT_EXPR)
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=current_user)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


def login_user(userid, password):
    logger.info("User Login")
    try:
        user_data = User.query.filter_by(userid=userid).one()
        if not user_data.check_password(password):
            logger.error("Authentication error: Wrong userid or password")
            return {'message': 'Authentication error: Wrong userid or password', "authenticated": False}, 401
        # Set JWT_ACCESS_TOKEN_EXPIRES to change token duration.
        access_token = create_access_token(identity=user_data)
        refresh_token = create_refresh_token(identity=user_data)
        logger.info("Access token created")
        logger.debug(f'access_token: {access_token}')
        resp = {
            'login': True,
            'msg': 'New login',
            'access_token': access_token,
            # 'refresh_token': refresh_token
        }
        _set_cookies(access_token, refresh_token)
        return resp, 200
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())
        raise e
