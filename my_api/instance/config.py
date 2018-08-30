
class Config(object):
    DEBUG = False
    SECRET = 'SECRET'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
