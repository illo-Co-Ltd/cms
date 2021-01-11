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


"""
@app.route("/api/auth/signup", methods=['POST'])
def auth_signup():
    logger.info("SignUp!")
    logger.info(request.get_json())

    data = request.get_json()

    username = data.get('username')
    useremail = data.get('useremail')
    userpwd = data.get('userpwd')
    bio = data.get('bio')

    user_data = user_model.User.query.filter_by(username=username).first()
    if user_data is not None:
        logger.info("Username is Already exist")
        return {"success": "username is already exist"}

    try:
        user = user_model.User(**data)
        user.has_password()
        user_model.db.session.add(user)
        user_model.db.session.commit()
        user_model.db.session.remove()
        logger.info("user Save Success")
        return {'success': 'user Save Success'}
    except Exception as e:
        logger.error("user Save Fail")
        logger.debug(traceback.print_exc(e))
        return {'fail': "user Save Fail"}


@app.route("/api/auth/login", methods=['POST'])
def auth_login():
    logger.info("User auth Login")
    logger.info(request.get_json())

    username = request.get_json()['username']
    useremail = request.get_json().get('useremail')
    userpwd = request.get_json()['userpwd']

    my_user = user_model.User()

    try:
        user_data = my_user.query.filter_by(username=username).first()

        if user_data is not None:
            auth = user_data.check_password(userpwd)
            if not auth:
                logger.info("password validation fail!")
                return {'status': 'fail'}, 401
            else:
                logger.info("login success!")
                session['login'] = True
                return {'success': session['login']}, 200
        else:
            logger.info("user information is wrong or user does  not exists....")
            return {'status': 'fail'}, 401
    except Exception as e:
        logger.error("login Exception...")
        logger.debug(traceback.print_exc(e))
        return {'status': 'fail'}, 404


@app.route('/api/auth/logout')
def auth_logout():
    session['login'] = False
    return {'success': 'logout'}

"""
@auth_route.route('/register', methods=['POST'])
def register_user():
    logger.info("user register")
    data = request.get_json()
    db = user_model.db

    user_data = user_model.User.query.filter_by(username=data.get('username')).first()
    if user_data is not None:
        logger.error("Username already exists")
        return {"failed": "username is already exist"}
    user = user_model.User(**data)
    user.has_password()
    db.session.add(user)
    db.session.commit()

    logger.info("User registration successful")

    return jsonify(user.to_dict()), 200


@auth_route.route('/login', methods=['POST'])
def login():
    logger.info("User Login")

    data = request.get_json()
    user_data = user_model.User.query.filter_by(username=data.get('username')).first()

    if user_data is not None:
        auth = user_data.check_password(data.get("userpwd"))

        if not auth:
            logger.error("Authentication valid error")
            return jsonify({'message': 'Authentication valid error', "authenticated": False}), 401

        logger.info("User Authentication token setting")
        token = jwt.encode({
            'sub': user_data.username,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, 'qwersdaiofjhoqwihlzxcjvjl')

        logger.info("Set up Success")
        logger.debug(token.decode('UTF-8'))
        return jsonify({"token": token.decode('UTF-8')})
    else:
        logger.error("User Does Not Exist")
        return jsonify({'message': 'User Does Not Exist', "authenticated": False}), 401


@auth_route.route('/logout', methods=['POST'])
def logout():
    return jsonify("Bye!")


@auth_route.route('/get_user', methods=['GET'])
def get_login_user():
    return jsonify("hi!")
