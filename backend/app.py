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

app.register_blueprint(auth_route, url_prefix='/api/auth')
app.register_blueprint(device_route, url_prefix='/api/device')
app.register_blueprint(image_route, url_prefix='/api/image')


# sanity check route
@app.route('/', methods=['GET'])
def test_router():
    logger.info("hello this is root url!")
    return jsonify('This is Docker Test developments Server!')

@app.route('/dbcreate', methods=['GET'])
def db_create():
    db.create_all()
    return jsonify('')

@app.route('/dbcheck', methods=['POST'])
def db_check():
    logger.info(app.config["SQLALCHEMY_DATABASE_URI"])
    # test
    data = request.get_json()
    logger.info(data)
    user = user_model.User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify('')

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


if __name__ == '__main__':
    # load environment variables
    load_dotenv(verbose=True)
    print(list(os.environ))
    app.run(host='0.0.0.0', port=os.getenv('FLASK_RUN_PORT'), debug=os.getenv('FLASK_DEBUG'))
