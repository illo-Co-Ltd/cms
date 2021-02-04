from functools import wraps
import jwt
from flask import request, jsonify, current_app
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from model.user_model import User
from util.logger import logger


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", '').split()
        logger.info(auth_headers)
        try:
            if len(auth_headers) != 2:
                raise jwt.InvalidTokenError('Header length mismatch')
            token = auth_headers[1]
            payload = jwt.decode(token, current_app.config['SECRET_KEY'])
            logger.info(payload)
            subject = payload['sub']
            user = User.query.filter_by(userid=subject).one()
            return f(user, *args, **kwargs)
        except MultipleResultsFound:
            return jsonify({
                'message': "Multiple user found for token",
                'authenticated': False
            }), 401
        except NoResultFound:
            return jsonify({
                'message': "No user found for token",
                'authenticated': False
            }), 401
        except jwt.ExpiredSignatureError:
            return jsonify({
                'message': "expired Token. Reauthentication required",
                'authenticated': False
            }), 401
        except (jwt.InvalidTokenError, Exception) as e:
            logger.error(e)
            return jsonify({
                'message': "Invalid Token. Registration / authentication required",
                'authenticated': False
            }), 401

    return _verify
