#
# -*- coding: utf-8 -*-
#
# @adminor: Arrack
# @Date:   2020-05-25 18:22:09
# @Last modified by:   Arrack
# @Last Modified time: 2020-06-11 11:29:09
#

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from app.extensions import db
from app.forms import ArticleForm
from app.forms import LoginForm
from app.models import Article
from app.models import Category
from app.models import Tag
from app.models import User


bp = Blueprint('admin', __name__)


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('admin/index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            flash('Welcome, %s!' % user.username)
            print('Welcome, %s!' % user.username)
            return redirect(next)
        flash('Invalid email or password.', category='error')
    flash(form.errors, category='error')
    return render_template('admin/login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@bp.route('/articles')
def articles():
    atcs = Article.query.all()
    return render_template('admin/articles.html', articles=atcs)


@bp.route('/article/write')
def articleWrite():
    # atcs = Article.query.all()
    return render_template('admin/articleWrite.html')


@bp.route('/article/<int:aid>', methods=['GET', 'POST'])
def articleEdit(aid):
    article = Article.query.get(aid)
    form = ArticleForm(request.form)
    tags = [item.tag.name for item in article.tags]

    if request.method == 'POST' and form.validate():
        article.title = form.title.data
        article.content = form.content.data
        article.category = Category.query.filter_by(name=form.category.data).first()

        updateTags = form.tags.data.split(',')

        # 将新标签写入数据库，并为文章添加新标签
        newTags = form.newTags.data
        if newTags:
            for t in newTags.split(','):
                if not Tag.exist(t):
                    tag = Tag(name=t.strip())
                    db.session.add(tag)
                    article.addTag(tag)

        # 对文章已有标签检测是否有更改
        tagsNeedDel = list(set(tags).difference(set(updateTags)))  # 需要移除的 tag
        tagsNeedAdd = list(set(updateTags).difference(set(tags)))  # 需要添加的 tag

        # 添加
        for t in tagsNeedAdd:
            tag = Tag.query.filter_by(name=t.strip()).first()
            article.addTag(tag)

        # 删除
        for t in tagsNeedDel:
            tag = Tag.query.filter_by(name=t.strip()).first()
            article.delTag(tag)

        db.session.commit()
        return redirect(url_for('admin.articles'))
    return render_template('admin/articleWrite.html', form=form, article=article, tags=tags)
