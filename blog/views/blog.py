from flask import Blueprint, send_from_directory, render_template
from flask_login import current_user

from blog.forms import LeaveMsgForm
from blog.models import LeaveMsg, Article
from blog.extensions import db

bp = Blueprint('blog', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    articles = Article.query.filter_by(verified=True).all()
    return render_template('blog/index.html', articles=articles)


@bp.route('/article/<year>/<month>/<title>')
def article(year, month, title):
    article = Article.query.filter_by(title=title).first()
    return render_template(
        'generated/{}/{}/{}.html'.format(
            year, month, title), article=article)


@bp.route('/category')
def categories():
    return send_from_directory(
        'static', 'generated/page/categories.html')


@bp.route('/category/<category>')
def category_articles(category):
    return send_from_directory(
        'static',
        'generated/page/category/{}.html'.format(category))


# @bp.route('/tag')
# def tags():
#     return send_from_directory(
#         'static', 'generated/page/tags.html')


# @bp.route('/tag/<tag>')
# def tag_articles(tag):
#     return send_from_directory(
#         'static', 'generated/page/tag/{}.html'.format(tag))


# @bp.route('/about')
# def about():
#     return send_from_directory(
#         'static', 'generated/page/about.html')


# @bp.route('/whatsonyourmind')
# def leavemsgs():
#     form = LeaveMsgForm()
#     messages = LeaveMsg.query.all()
#     # if not current_user.is_authenticated:
#     # if form.validate_on_submit():
#     #     return
#     return render_template('blog/leavemsgs.html', form=form, messages=messages)
