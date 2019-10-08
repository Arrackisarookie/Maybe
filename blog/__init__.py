from flask import Flask, render_template

from blog.admin import admin
from blog.extensions import (
    db, loginmanager, migrate, moment
)

from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_blueprint(app)
    register_extensions(app)
    # register_errors(app)

    admin.init_app(app)

    return app


def register_extensions(app):
    db.init_app(app)
    loginmanager.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)


def register_blueprint(app):
    from .views import blog
    app.register_blueprint(blog.bp)
    from .views import auth
    app.register_blueprint(auth.bp, url_prefix='/auth')


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html')

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html')
