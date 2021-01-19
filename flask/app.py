import os

from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from route.auth import auth_route
from route.check import check_route
from route.crud import crud_route
from route.image import image_route
from route.camera import camera_route

from util.logger import logger

global logger


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
    with app.app_context():
        from model import db_base
        db_base.db.init_app(app)
        db_base.db.create_all()

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    app.register_blueprint(check_route, url_prefix='/')
    app.register_blueprint(auth_route, url_prefix='/auth')
    app.register_blueprint(crud_route, url_prefix='/api')
    app.register_blueprint(camera_route, url_prefix='/api/camera')

    return app


if __name__ == '__main__':
    logger.info('Loaded ENV:' + str(list(os.environ)))

    app = create_app()
    app.run(host='0.0.0.0',
            port=os.getenv('FLASK_RUN_PORT'),
            debug=os.getenv('FLASK_DEBUG'))
