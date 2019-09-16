import os
import click

from flask import Flask

from .extensions import db
from .settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('blog')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprint(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprint(app):
    from .blueprints import blog
    app.register_blueprint(blog.bp)


def register_commands(app):
    # 初始化，创建空表
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        import blog.models
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initilized database.')

    # 插入测试数据
    @app.cli.command()
    @click.option(
        '--category', default=5, help='Quantity of categories, default is 5')
    @click.option(
        '--post', default=20, help='Quantity of posts, default is 20')
    @click.option(
        '--comment', default=100, help='Quantity of comments, default is 100')
    def forge(category, post, comment):
        from blog.fakes import (
            fake_admin, fake_categories, fake_posts, fake_comments
        )
        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Done.')
