import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'nicearrack@163.com'
    ADMIN_NAME = os.environ.get('ADMIN_NAME') or 'Arrack'

    SITE_TITLE = 'Maybe'
    SITE_SUBTITLE = 'Everything is not too late.'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 280

    ARTICLES_PER_PAGE = 10
    TALKS_PER_PAGE = 15
    COMMENTS_PER_PAGE = 5

    JSON_AS_ASCII = False

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
