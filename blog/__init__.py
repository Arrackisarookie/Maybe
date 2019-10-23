import click
from flask import Flask, current_app, jsonify, render_template, request

from blog.admin import admin
from blog.models.user import Role, User
from blog.extensions import (
    db, loginmanager, migrate, moment)

from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_blueprint(app)
    register_extensions(app)
    register_errors(app)
    register_command(app)

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
    from .api import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


def register_errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            response = jsonify({'error': 'not found'})
            response.status_code = 404
            return response
        return render_template('errors/404.html'), 404


def register_command(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm(
                'This operation will delete the database, '
                'do you want to continue?')
            db.drop_all()
            click.echo('All tables have been dropped.')
        db.create_all()
        click.echo('Initialized database.')
        Role.init_roles()
        click.echo('Initialized Roles.')

    @app.cli.command()
    @click.argument('username')
    @click.argument('password')
    def initadmin(username, password):
        email = current_app.config['ADMIN_EMAIL']
        if User.query.first():
            click.echo('Administrator already exsits.')
            return None
        user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        click.echo('Initialized Administrator %s' % username)
