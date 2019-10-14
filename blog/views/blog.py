from os.path import join

from flask import Blueprint, render_template, flash, redirect, url_for

from blog.models import About, Article, Category, Tag, Talk, Top
from blog.utils import markdown_to_html
from blog.forms import TalkForm
from blog.extensions import db


bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    articles = Article.query.order_by(Article.id.desc()).all()
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
    articles = Category.query.filter_by(name=category).first().articles.order_by(Article.id.desc())
    return render_template(
        'blog/category.html', category=category, articles=articles)


@bp.route('/tag/<tag>')
def tag(tag):
    articles = Tag.query.filter_by(name=tag).first().articles.order_by(Article.id.desc())
    return render_template(
        'blog/tag.html', tag=tag, articles=articles)


@bp.route('/about')
def about():
    about = About.query.first()
    about_body = markdown_to_html(about.body)
    return render_template('blog/about.html', about=about, about_body=about_body)


@bp.route('/talktalk', methods=['GET', 'POST'])
def talktalk():
    form = TalkForm()
    if form.validate_on_submit():
        talk = Talk(
            content=form.content.data,
            private=form.private.data)
        db.session.add(talk)
        db.session.commit()
        flash('能比比尽量别动手。')
        return redirect(url_for('blog.talktalk'))

    first_id = Top.query.filter_by(type='talk').first().foreign_id
    first = Talk.query.filter_by(id=first_id).first()

    # TODO private, auth, flash, style
    talks = Talk.query.filter(Talk.id != first_id).order_by(Talk.id.desc()).all()
    return render_template('blog/talktalk.html', first=first, talks=talks, form=form)
