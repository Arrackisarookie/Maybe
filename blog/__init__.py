import os
import click

from flask import Flask, render_template

from blog.extensions import bootstrap, db
from blog.settings import config
from blog.models import Admin, Category, Comment, Article


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('blog')
    print(config_name.capitalize(), 'mode.')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprint(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)

    return app


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(
            db=db, Admin=Admin, Article=Article, Category=Category, Comment=Comment
        )


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)


def register_blueprint(app):
    from blog.views import blog
    app.register_blueprint(blog.bp)


def register_commands(app):
    # 初始化，创建空表
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
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
        '--article', default=20, help='Quantity of articles, default is 20')
    @click.option(
        '--comment', default=100, help='Quantity of comments, default is 100')
    def forge(category, article, comment):
        from blog.fakes import (
            fake_admin, fake_categories, fake_articles, fake_comments
        )
        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d articles...' % article)
        fake_articles(article)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Done.')


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
