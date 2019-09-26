from flask import Blueprint, send_from_directory, render_template

from blog.forms import LeaveMsgForm

bp = Blueprint('blog', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    return send_from_directory(
            'static', 'generated/page/index.html')


@bp.route('/tag')
def tags():
    return send_from_directory(
        'static', 'generated/page/tags.html')


@bp.route('/tag/<tag>')
def tag_articles(tag):
    return send_from_directory(
        'static', 'generated/page/tag/{}.html'.format(tag))


@bp.route('/category')
def categories():
    return send_from_directory(
        'static', 'generated/page/categories.html')


@bp.route('/category/<category>')
def category_articles(category):
    return send_from_directory(
        'static',
        'generated/page/category/{}.html'.format(category))


@bp.route('/about')
def about():
    return send_from_directory(
        'static', 'generated/page/about.html')


@bp.route('/article/<year>/<month>/<article>')
def article(year, month, article):
    return send_from_directory(
        'static',
        'generated/article/{}/{}/{}.html'.format(
            year, month, article))


@bp.route('/whatsonyourmind')
def leavemsgs():
    form = LeaveMsgForm()
    return render_template('blog/leavemsgs.html')
