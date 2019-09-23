import os
import sys

from flask import Flask, render_template

from blog.generate import Generate


def create_app():

    app = Flask(__name__)
    # app.config.from_object('config')

    register_blueprint(app)

    return app


gen = Generate()
gen.main()


def register_blueprint(app):
    from .views import blog
    app.register_blueprint(blog.bp)


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
