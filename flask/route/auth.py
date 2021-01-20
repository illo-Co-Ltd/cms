"""
url route split
"""
import traceback
from flask import Blueprint, request, jsonify, session, current_app
from util.logger import logger
from model import user_model

import jwt
import datetime

auth_route = Blueprint('auth_route', __name__)


@auth_route.route('/register', methods=['POST'])
def register_user():
    logger.info("user register")
    data = request.get_json()
    db = user_model.db

    user_data = user_model.User.query.filter_by(userid=data.get('userid')).first()
    if user_data is not None:
        logger.error("Userid already exists")
        return {"failed": "userid already exists"}

    try:
        user = user_model.User(**data)
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        logger.info('User registration successful')
        return jsonify(user.to_dict()), 200
    except Exception as e:
        logger.error("user Save Fail")
        logger.debug(traceback.print_exc(e))
        return {'User registration failed'}, 200


@auth_route.route('/login', methods=['POST'])
def login():
    logger.info("User Login")

    data = request.get_json()
    user_data = user_model.User.query.filter_by(userid=data.get('userid')).first()

    if user_data is not None:
        auth = user_data.check_password(data.get("password"))

        if not auth:
            logger.error("Authentication valid error")
            return jsonify({'message': 'Authentication valid error', "authenticated": False}), 401

        logger.info("User Authentication token setting")
        token = jwt.encode({
            'sub': user_data.userid,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, 'qwersdaiofjhoqwihlzxcjvjl')

        logger.info("Set up Success")
        logger.debug(token.decode('UTF-8'))
        session['userid'] = user_data.userid
        return jsonify({"token": token.decode('UTF-8')})
    else:
        logger.error("User Does Not Exist")
        return jsonify({'message': 'User Does Not Exist', "authenticated": False}), 401


@auth_route.route('/logout', methods=['POST'])
def logout():
    session.pop('userid', None)
    return jsonify("Bye!")


@auth_route.route('/get_user', methods=['GET'])
def get_login_user():
    try:
        return jsonify({'userid':session['userid']})
    except:
        return jsonify({'Status':'Not logged in'})

