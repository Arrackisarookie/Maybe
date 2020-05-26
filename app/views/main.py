#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-25 18:22:18
# @Last modified by:   Arrack
# @Last Modified time: 2020-05-26 16:29:08
#

from os.path import join

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for

from app.extensions import db
from app.forms import TalkForm
from app.models.article import Article
from app.models.article import Category
from app.models.article import Tag
from app.utils import markdown_to_html


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    articles = Article.query.order_by(Article.id.desc()).all()
    return render_template('main/index.html', articles=articles)


@bp.route('/article')
def article():
    return render_template('main/article.html')


@bp.route('/category')
def category():
    return render_template('main/category.html')


@bp.route('/about')
def about():
    return render_template('main/about.html')


@bp.route('/shuoshuo')
def shuoshuo():
    return render_template('main/shuoshuo.html')



# @bp.route('/article/<year>/<month>/<title>')
# def article(year, month, title):
#     url = join('/article', year, month, title)
#     article = Article.query.filter_by(url=url).first()
#     article_body = markdown_to_html(article.body)
#     return render_template(
#         'blog/article.html', article=article, article_body=article_body)


# @bp.route('/category/<category>')
# def category(category):
#     articles = Category.query.filter_by(name=category).first().articles.order_by(Article.id.desc())
#     return render_template(
#         'blog/category.html', category=category, articles=articles)


# @bp.route('/tag/<tag>')
# def tag(tag):
#     articles = Tag.query.filter_by(name=tag).first().articles.order_by(Article.id.desc())
#     return render_template(
#         'blog/tag.html', tag=tag, articles=articles)


# @bp.route('/talktalk', methods=['GET', 'POST'])
# def talktalk():
#     form = TalkForm()
#     if form.validate_on_submit():
#         talk = Talk(
#             content=form.content.data,
#             private=form.private.data)
#         db.session.add(talk)
#         db.session.commit()
#         flash('能比比尽量别动手。')
#         return redirect(url_for('blog.talktalk'))

#     first_id = Top.query.filter_by(type='talk').first().foreign_id
#     first = Talk.query.get(first_id).first()

#     # TODO private, auth, flash, style
#     talks = Talk.query.filter(Talk.id != first_id).order_by(Talk.id.desc()).all()
#     return render_template('blog/talktalk.html', first=first, talks=talks, form=form)
