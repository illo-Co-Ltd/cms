import os
import datetime


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    # flask
    DEBUG = True
    FLASK_APP = 'app.py'
    FLASK_RUN_PORT = 5000
    BASE_URL = 'localhost:8080'

    # router
    SWAGGER_UI_DOC_EXPANSION = 'list'

    # ORM
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1010@db:3306/cms'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # jwt auth
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_COOKIE_SECURE = False
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=14)
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/'
    JWT_ALGORITHM = 'HS256'
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_SECURE = False
    TOKEN_EXPR_SECS = 1800


class TestingConfig(Config):
    TESTING = True


configmap = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'test': TestingConfig
}
