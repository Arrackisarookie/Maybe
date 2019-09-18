import os


ENGINE = 'mysql'
DRIVER = 'pymysql'

MYSQL_USERNAME = 'Arrack'
MYSQL_PASSWORD = 'whosyourdaddy'
MYSQL_HOST = 'Arrack.mysql.pythonanywhere-services.com'
MYSQL_DATABASE = 'Arrack$blog'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BLOG_ARTICLE_PER_PAGE = 5
    BLOG_MANAGE_ARTICLE_PER_PAGE = 10
    BLOG_COMMENT_PER_PAGE = 10


class DevelopmentConfig(BaseConfig):
    # 'mysql+pymysql://username:password@localhost/db_name'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/blog-dev'


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/blog-test'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}/{}?charset=utf8'.format(
        ENGINE, DRIVER,
        MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
