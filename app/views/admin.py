#
# -*- coding: utf-8 -*-
#
# @adminor: Arrack
# @Date:   2020-05-25 18:22:09
# @Last modified by:   Arrack
# @Last Modified time: 2020-06-08 17:00:25
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
from app.models import ArticleTag
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
            flash('Welcome, %s!' % user.nickName)
            print('Welcome, %s!' % user.nickName)
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


@bp.route('/article/<int:aid>/edit', methods=['GET', 'POST'])
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
        newTags = form.newTags.data.split(',')
        for t in newTags:
            tag = Tag.query.filter_by(name=t.strip()).first()
            if tag is None:
                tag = Tag(name=t.strip())
                db.session.add(tag)
                at = ArticleTag(article=article, tag=tag)
                db.session.add(at)

        # 对文章已有标签检测是否有更改
        tagsNeedDel = list(set(tags).difference(set(updateTags))) # 需要移除的 tag
        tagsNeedAdd = list(set(updateTags).difference(set(tags))) # 需要添加的 tag

        # todo: 整合到 Model 中
        # 添加
        for t in tagsNeedAdd:
            tag = Tag.query.filter_by(name=t.strip()).first()
            at = ArticleTag(article=article, tag=tag)
            db.session.add(at)

        # 删除
        for t in tagsNeedDel:
            tag = Tag.query.filter_by(name=t.strip()).first()
            at = article.tags.filter_by(tagID=tag.id).first()
            if at:
                db.session.delete(at)
        db.session.commit()
        return redirect(url_for('admin.articles'))
    return render_template('admin/articleWrite.html', form=form, article=article, tags=tags)
