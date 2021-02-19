import traceback
from flask import Blueprint, request, jsonify, session, current_app, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, current_user
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from model.db_base import db
from model.user_model import User
from model.company_model import Company

from app import jwt
from util.logger import logger

auth_route = Blueprint('auth_route', __name__)
jwt = current_app.extensions['flask-jwt-extended']


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@auth_route.route("/whoami", methods=["GET"])
@jwt_required()
def whoami():
    return jsonify(
        id=current_user.id,
        userid=current_user.userid,
        username=current_user.username,
        company=current_user.company
    )


@auth_route.route('/register', methods=['POST'])
def register_user():
    logger.info("user register")
    data = request.get_json()
    try:
        comp_name = data.get('company')
        if comp_name is None:
            raise ValueError('Company name is empty.')
        data.update({'company': Company.query.filter_by(name=comp_name).one().id})

        user_data = User.query.filter_by(userid=data.get('userid')).first()
        if user_data is not None:
            logger.error("Userid already exists")
            return jsonify({
                'message': 'User registration failed',
                'reason': 'userid already exists'
            }), 200

        user = User(**data)
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
    user_data = User.query.filter_by(userid=data.get('userid')).first()

    if user_data is not None:
        if not user_data.check_password(data.get("password")):
            logger.error("Authentication error: Wrong userid or password")
            return jsonify({'message': 'Authentication error: Wrong userid or password', "authenticated": False}), 401

        access_token = create_access_token(identity=user_data)
        logger.info("Access token created")
        logger.debug(f'access_token: {access_token}')
        session['userid'] = user_data.userid
        return jsonify(access_token=access_token)
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
