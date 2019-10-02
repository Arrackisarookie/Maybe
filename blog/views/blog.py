from flask import Blueprint, send_from_directory, render_template

from blog.forms import LeaveMsgForm
from blog.models import LeaveMsg, Article, Category, Tag

bp = Blueprint('blog', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    articles = Article.query.all()
    return render_template('blog/index.html', articles=articles)


@bp.route('/article/<year>/<month>/<title>')
def article(year, month, title):
    article = Article.query.filter_by(title=title)
    return render_template(
        'generated/{}/{}/{}.html'.format(
            year, month, title), article=article)


@bp.route('/category/<category>')
def category(category):
    articles = Category.query.filter_by(name=category).first().articles
    return render_template(
        'blog/category.html', category=category, articles=articles)


@bp.route('/tag/<tag>')
def tag_articles(tag):
    articles = Tag.query.filter_by(name=tag).first().articles
    return render_template(
        'blog/tag.html', tag=tag, articles=articles)


@bp.route('/about')
def about():
    return send_from_directory(
        'static', 'generated/page/about.html')


@bp.route('/whatsonyourmind')
def leavemsgs():
    form = LeaveMsgForm()
    messages = LeaveMsg.query.all()
    # if not current_user.is_authenticated:
    # if form.validate_on_submit():
    #     return
    return render_template('blog/leavemsgs.html', form=form, messages=messages)
