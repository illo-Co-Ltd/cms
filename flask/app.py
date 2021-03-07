import os

from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flaskconfig import *

from util.logger import logger

# instantiate the app
# from flask_restplus import Api, Resource, fields

app = Flask(__name__)
# api = Api(app, version='1.0', title='illo API', description='API for DB access and device control')

try:
    app.config.from_object(configmap[app.config['ENV']]())
except KeyError:
    logger.error('Improper ENV name for config')
    exit()

# initialize db
with app.app_context():
    from models import db_base

    db_base.db.init_app(app)
    db_base.db.create_all()

    if app.env == 'development':
        from models import Company, Device, User
        import datetime

        db = db_base.db
        if Company.query.first() is None:
            company = Company(
                name='illo',
                subscription=1,
                expiration_date=datetime.datetime.now() + datetime.timedelta(days=365))
            db.session.add(company)
            db.session.commit()
        if Device.query.first() is None:
            device = Device(
                model='Prototype1',
                serial='testserial1234',
                company=Company.query.filter_by(name='illo').first().id)
            db.session.add(device)
            db.session.commit()

# enable CORS
CORS(app, resources={r'*': {'origins': '*'}}, supports_credentials=True)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)


def add_blueprints():
    from api.auth import auth_route
    from api.check import check_route
    from api.db import db_route
    from api.camera import camera_route
    from tasks.task_callback import task_callback_route

    app.register_blueprint(check_route, url_prefix='/')
    app.register_blueprint(auth_route, url_prefix='/auth')
    app.register_blueprint(db_route, url_prefix='/api')
    app.register_blueprint(camera_route, url_prefix='/api/camera')
    app.register_blueprint(task_callback_route, url_prefix='/task_callback')


jwt = None
if __name__ == '__main__':
    logger.info('Loaded ENV:' + str(list(os.environ)))
    with app.app_context():
        add_blueprints()
    app.run(host='0.0.0.0',
            port=os.getenv('FLASK_RUN_PORT'),
            debug=os.getenv('FLASK_DEBUG'))
