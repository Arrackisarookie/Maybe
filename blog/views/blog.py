from flask import Blueprint, send_from_directory, render_template, current_app

from blog.models import Article, Category, Tag
from blog.utils import markdown_to_html

bp = Blueprint('blog', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    articles = Article.query.all()
    title = current_app.config['SITE_TITLE']
    subtitle = current_app.config['SITE_SUBTITLE']
    return render_template('blog/index.html', articles=articles, title=title, subtitle=subtitle)


@bp.route('/article/<year>/<month>/<title>')
def article(year, month, title):
    article = Article.query.filter_by(title=title).first()
    article_body = markdown_to_html(article.markdown_path, article.filename)
    return render_template(
        'blog/article.html', article=article, article_body=article_body)


@bp.route('/category/<category>')
def category(category):
    articles = Category.query.filter_by(name=category).first().articles
    return render_template(
        'blog/category.html', category=category, articles=articles)


@bp.route('/tag/<tag>')
def tag(tag):
    articles = Tag.query.filter_by(name=tag).first().articles
    return render_template(
        'blog/tag.html', tag=tag, articles=articles)


@bp.route('/about')
def about():
    return send_from_directory(
        'static', 'generated/page/about.html')
