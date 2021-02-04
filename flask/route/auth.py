import traceback
from flask import Blueprint, request, jsonify, session, current_app
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from util.logger import logger
from model import user_model
from model import company_model

import jwt
import datetime

auth_route = Blueprint('auth_route', __name__)


@auth_route.route('/register', methods=['POST'])
def register_user():
    db = user_model.db
    logger.info("user register")
    data = request.get_json()
    try:
        comp_name = data.get('company')
        if comp_name is None:
            raise ValueError('Company name is empty.')
        data.update({'company': company_model.Company.query.filter_by(name=comp_name).one().id})

        user_data = user_model.User.query.filter_by(userid=data.get('userid')).first()
        if user_data is not None:
            logger.error("Userid already exists")
            return jsonify({
                'message': 'User registration failed',
                'reason': 'userid already exists'
            }), 200

        user = user_model.User(**data)
        user.hash_password()
        db.session.add(user)
        db.session.commit()

        logger.info('User registration successful')
        return jsonify({
            'message': 'User registration successful',
        }), 200

    except Exception as e:
        logger.error("User registration failed")
        logger.debug(traceback.format_exc())
        return jsonify({
            'message': 'User registration failed',
            'reason': str(e)
        }), 200


@auth_route.route('/login', methods=['POST'])
def login():
    logger.info("User Login")
    if session.get('userid') is not None:
        return jsonify({'message': f'Already logged in with {session.get("userid")}'}), 200

    data = request.get_json()
    user_data = user_model.User.query.filter_by(userid=data.get('userid')).first()

    if user_data is not None:
        if not user_data.check_password(data.get("password")):
            logger.error("Authentication error: Wrong userid or password")
            return jsonify({'message': 'Authentication error: Wrong userid or password', "authenticated": False}), 401

        logger.info("User Authentication token setting")
        token = jwt.encode({
            'sub': user_data.userid,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=current_app.config['TOKEN_EXPR_SECS'])
        }, current_app.config['SECRET_KEY'])

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
        return jsonify({'userid': session.get('userid')})
    except:
        return jsonify({'Status': 'Not logged in'})
