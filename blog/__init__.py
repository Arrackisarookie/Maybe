from flask import Flask, render_template
from flask_login import LoginManager

from blog.generate import Generate


gen = Generate()
gen()


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    register_blueprint(app)
    register_login(app)

    return app


def register_login(app):
    lm = LoginManager()

    @lm.user_loader
    def load_user(username):
        from blog.views.admin import query_user, User
        if query_user(username) is not None:
            cur_user = User
            cur_user.id = username
            return cur_user
        return None

    lm.login_view = 'admin.login'
    lm.login_message = '你特娘的请登录啊，管理员'
    lm.init_app(app)


def register_blueprint(app):
    from .views import blog
    app.register_blueprint(blog.bp)
    from .views import admin
    app.register_blueprint(admin.bp)
    from .views import api
    app.register_blueprint(api.bp)


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
