import os
import sys

from flask import Flask, render_template
from flask_login import LoginManager
from blog.generate import Generate


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    register_blueprint(app)

    lm.init_app(app)

    return app


lm = LoginManager()
lm.login_view = 'admin.login'
lm.login_message = '你特娘的请登录啊，管理员'

gen = Generate()
gen.main()


def register_blueprint(app):
    from .views import blog
    app.register_blueprint(blog.bp)
    from .views import admin
    app.register_blueprint(admin.bp)


def register_errors(app):
    # @app.errorhandler(400)
    # def bad_request(e):
    #     return render_template('errors/400.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html')

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html')
