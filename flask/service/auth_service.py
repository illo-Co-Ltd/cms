from flask import after_this_request
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies

from model.model_import import User
from util.logger import logger


def _set_cookies(access_token, refresh_token):
    @after_this_request
    def _internal(response):
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response


def login_user(data):
    logger.info("User Login")
    user_data = User.query.filter_by(userid=data.get('userid')).first()

    if user_data is not None:
        if not user_data.check_password(data.get("password")):
            logger.error("Authentication error: Wrong userid or password")
            return {'message': 'Authentication error: Wrong userid or password', "authenticated": False}, 401

        access_token = create_access_token(identity=user_data)
        refresh_token = create_refresh_token(identity=user_data)
        logger.info("Access token created")
        logger.debug(f'access_token: {access_token}')
        resp = {
            'login': True,
            'msg': 'New login',
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        _set_cookies(access_token, refresh_token)
        return resp, 200
    else:
        logger.error("User Does Not Exist")
        return {'message': 'User Does Not Exist', "authenticated": False}, 401
