import os
from dotenv import load_dotenv

from flask import Flask, jsonify, request, session, Response
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from router.api.auth import auth_route
from router.api.check import check_route
from router.api.device import device_route
from router.api.image import image_route

from model import user_model, device_model, image_model

from util.logger import logger


def create_app():
    # instantiate the app
    app = Flask(__name__)
    app.secret_key = 'laksdjfoiawjewfansldkfnzcvjlzskdf'

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_COOKIE_CSRF_PROTECT'] = os.getenv('JWT_COOKIE_CSRF_PROTECT')
    app.config['JWT_COOKIE_SECURE'] = os.getenv('JWT_COOKIE_SECURE')
    app.config['SECRET_KEY'] = 'qwersdaiofjhoqwihlzxcjvjl'

    # initialize db
    user_model.db.init_app(app)
    device_model.db.init_app(app)
    image_model.db.init_app(app)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    app.register_blueprint(check_route, url_prefix='')
    app.register_blueprint(auth_route, url_prefix='/api/auth')
    app.register_blueprint(device_route, url_prefix='/api/device')
    app.register_blueprint(image_route, url_prefix='/api/image')

    return app


if __name__ == '__main__':
    # load environment variables
    load_dotenv(verbose=True)
    logger.info('Loaded ENV:' + str(list(os.environ)))

    app = create_app()
    app.run(host='0.0.0.0',
            port=os.getenv('FLASK_RUN_PORT'),
            debug=os.getenv('FLASK_DEBUG'))

