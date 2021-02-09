class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'mysql://user@localhost/foo'


class TestingConfig(Config):
    TESTING = True
