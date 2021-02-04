import jwt
from flask import request, jsonify, current_app
from model.user_model import User
from util.logger import logger
from functools import wraps


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", '').split()

        invalid_msg = {
            'message': "Invalid Token. Registeration / authentication required",
            'authenticated': False
        }

        expired_msg = {
            'message': "expired Token. Reauthentication required",
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            parse_name = data['sub']
            user = User.query.filter_by(username=parse_name).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            logger.error(e)
            return jsonify(invalid_msg), 401

    return _verify
