import os


MYSQL_USERNAEM = 'root'
MYSQL_PASSWORD = ''
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = '3306'
MYSQL_DATABASE = 'Blog'
MYSQL_DEV_DATABASE = 'Blog-dev'

prefix = 'mysql+pymysql://'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_MANAGE_POST_PER_PAGE = 15
    BLUELOG_COMMENT_PER_PAGE = 15


class DevelopmentConfig(BaseConfig):
    # 'mysql+pymysql://username:password@localhost/db_name'
    SQLALCHEMY_DATABASE_URI = prefix + '%s:%s@%s:%s/%s' % (MYSQL_USERNAEM, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DEV_DATABASE)


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/memory'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + '%s:%s@%s/%s' % (MYSQL_USERNAEM, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
