from datetime import datetime, timedelta, timezone
import traceback
from flask import Blueprint, request, jsonify, session, current_app, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    jwt_required, current_user, unset_jwt_cookies, get_jwt, get_jwt_identity, verify_jwt_in_request
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from models.db_base import db
from models.user_model import User
from models.company_model import Company

from app import jwt
from util.logger import logger

auth_route = Blueprint('auth_route', __name__)
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


@auth_route.route("/whoami", methods=["GET"])
@jwt_required()
def whoami():
    logger.info(f'Who am I? : {current_user}')
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
@jwt_required(optional=True)
def login():
    logger.info("User Login")
    '''
    try:
        verify_jwt_in_request()
        get_jwt_identity()
    '''
    logger.info(f'current_user:<{current_user}>')
    # flask에 로그인된 유저가 있을 때
    '''
    if current_user is not None:
        try:
            verify_jwt_in_request()
        except:
            pass
        access_token = create_access_token(identity=current_user)
        resp = jsonify({
            'login': True,
            'msg': f'Already logged in as {current_user}. Refreshing token.',
            'access_token': access_token,
        })
        set_access_cookies(resp, access_token)
        return resp, 200
        '''

    data = request.get_json()
    user_data = User.query.filter_by(userid=data.get('userid')).first()

    if user_data is not None:
        if not user_data.check_password(data.get("password")):
            logger.error("Authentication error: Wrong userid or password")
            return jsonify({'message': 'Authentication error: Wrong userid or password', "authenticated": False}), 401

        access_token = create_access_token(identity=user_data)
        refresh_token = create_refresh_token(identity=user_data)
        logger.info("Access token created")
        logger.debug(f'access_token: {access_token}')
        resp = jsonify({
            'login': True,
            'msg': 'New login',
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        #set_access_cookies(resp, access_token)
        #set_refresh_cookies(resp, refresh_token)
        return resp, 200
    else:
        logger.error("User Does Not Exist")
        return jsonify({'message': 'User Does Not Exist', "authenticated": False}), 401


@auth_route.after_request
def refresh_expiring_jwts(resp):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=current_user)
            #set_access_cookies(resp, access_token)
        return resp
    except (RuntimeError, KeyError):
        return resp


@auth_route.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({
        'msg': 'Logout successful.'
    })
    unset_jwt_cookies(resp)
    return resp
