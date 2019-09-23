import os
import sys

from flask import Flask, render_template, send_from_directory

from blog.generate import Generate


def create_app():

    app = Flask(__name__)
    # app.config.from_object('config')

    @app.route('/')
    @app.route('/index')
    def index():

        return send_from_directory(
            'static', 'generated/page/index.html')

    @app.route('/category')
    def categories():

        return send_from_directory(
            'static', 'generated/page/categories.html')

    @app.route('/article/<year>/<month>/<article>')
    def article(year, month, article):

        return send_from_directory(
            'static',
            'generated/article/{}/{}/{}.html'.format(
                year, month, article))
    return app


gen = Generate()
gen.main()


def register_blueprint(app):
    from blog.views import blog
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
