import os

SITE_TITLE = '也许'
SITE_SUBTITLE = 'Everything is not too late.'

ARTICLE_PATH = './blog/source/_article/'
PAGE_PATH = './blog/source/_page/'
FINISHED_PATH = './blog/source/_finished/'
GENERATED_PATH = './blog/static/generated/'

DEFAULT_CATEGORY = '未分类'
DEFAULT_TAG = ['其他']

BLOG_DAT = './blog/static/generated/data/'

UPLOADED_MARKDOWN_DEST = ARTICLE_PATH


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'

    SITE_TITLE = '也许'
    SITE_SUBTITLE = 'Everything is not too late.'

    ARTICLE_PATH = './blog/source/_article/'
    PAGE_PATH = './blog/source/_page/'
    FINISHED_PATH = './blog/source/_finished/'
    GENERATED_PATH = './blog/static/generated/'

    DEFAULT_CATEGORY = '未分类'
    DEFAULT_TAG = ['其他']

    UPLOADED_MARKDOWN_DEST = ARTICLE_PATH

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
