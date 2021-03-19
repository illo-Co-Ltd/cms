import os

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flaskconfig import *

from util.logger import logger

app = Flask(__name__)

try:
    app.config.from_object(configmap[app.config['ENV']]())
except KeyError:
    logger.error('Improper ENV name for config')
    exit()

# initialize db
with app.app_context():
    from model import db_base

    db_base.db.init_app(app)
    db_base.db.create_all()

    if app.env == 'development':
        from model import Company, Device, User
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

if __name__ == '__main__':
    logger.info('Loaded ENV:' + str(list(os.environ)))
    with app.app_context():
        from router import api
        from router.auth import bp as auth_bp
        api.init_app(app)
        app.register_blueprint(auth_bp)
    app.run(host='0.0.0.0',
            port=os.getenv('FLASK_RUN_PORT'),
            debug=os.getenv('FLASK_DEBUG'))
