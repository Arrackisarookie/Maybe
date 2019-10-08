import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'

    FLASK_ADMIN = os.environ.get('FLASK_ADMIN') or 'Arrack'

    FLASK_ADMIN_SWATCH = 'flatly'

    SITE_TITLE = 'Maybe'
    SITE_SUBTITLE = 'Everything is not too late.'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQL_ENGINE_PREFIX') + os.environ.get('DEV_DATABASE_URI')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQL_ENGINE_PREFIX') + os.environ.get('TEST_DATABASE_URI')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQL_ENGINE_PREFIX') + os.environ.get('DATABASE_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
