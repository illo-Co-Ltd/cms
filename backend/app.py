import os, traceback
from dotenv import load_dotenv

from flask import Flask, jsonify, request, session, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from router.api.auth import auth_route
from router.api.device import device_route
from router.api.image import image_route

from provider.baseball_scrapper import get_baseball_rank
from model import user_model

from util.logger import logger
from util.auth_util import token_required

# instantiate the app
app = Flask(__name__)
app.secret_key = 'laksdjfoiawjewfansldkfnzcvjlzskdf'

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_COOKIE_CSRF_PROTECT'] = os.getenv('JWT_COOKIE_CSRF_PROTECT')
app.config['JWT_COOKIE_SECURE'] = os.getenv('JWT_COOKIE_SECURE')
app.config['SECRET_KEY'] = 'qwersdaiofjhoqwihlzxcjvjl'

db = SQLAlchemy()
db.init_app(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.register_blueprint(auth_route, url_prefix='/api2/auth')
app.register_blueprint(device_route, url_prefix='/api/device')
app.register_blueprint(image_route, url_prefix='/api/image')


# sanity check route
@app.route('/', methods=['GET'])
def test_router():
    logger.info("hello this is root url!")
    return jsonify('This is Docker Test developments Server!')





@app.route('/user/list', methods=['GET'])
def list_user():
    logger.info("List all users")
    return jsonify('This is Docker Test developments Server!')

@app.route('/user/add', methods=['GET'])
def add_user():
    logger.info("Add user to database")
    return jsonify('This is Docker Test developments Server!')

@app.route('/user/delete', methods=['GET'])
def delete_user():
    logger.info("Delete user from database")
    return jsonify('This is Docker Test developments Server!')






@app.route('/health_check', methods=['GET'])
def health_check():
    logger.info("health check route url!")
    return jsonify('good')


@app.route('/baseball_data', methods=['GET'])
def new_data():
    logger.info("baseball_data route!")
    data_list = get_baseball_rank()
    return jsonify(data_list)


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


if __name__ == '__main__':
    # load environment variables
    load_dotenv(verbose=True)
    print(list(os.environ))
    app.run(host='0.0.0.0', port=os.getenv('FLASK_RUN_PORT'), debug=os.getenv('FLASK_DEBUG'))
