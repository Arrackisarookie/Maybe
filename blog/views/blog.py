from os.path import join

from flask import Blueprint, render_template

from blog.models import About, Article, Category, Tag
from blog.utils import markdown_to_html

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    articles = Article.query.all()
    return render_template('blog/index.html', articles=articles)


@bp.route('/article/<year>/<month>/<title>')
def article(year, month, title):
    url = join('/article', year, month, title)
    article = Article.query.filter_by(url=url).first()
    article_body = markdown_to_html(article.body)
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
    about = About.query.first()
    about_body = markdown_to_html(about.body)
    return render_template('blog/about.html', about=about, about_body=about_body)
