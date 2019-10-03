from datetime import datetime
import os

from flask import Blueprint, flash, redirect, render_template, url_for, current_app
from flask_login import login_required

from blog.extensions import upload_markdowns, db
from blog.forms import UpdateForm
from blog.models import Article, Category, Tag
from blog.utils import new_tag


bp = Blueprint('admin', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('admin/admin.html', title='admin-management')


@bp.route('/upload/article', methods=['GET', 'POST'])
@login_required
def upload_article():
    form = UpdateForm()
    if form.validate_on_submit():
        utcnow = datetime.utcnow()
        title = form.title.data
        subfolder = os.path.join(str(utcnow.year), str(utcnow.month))
        markdown_path = os.path.join(current_app.config['MARKDOWN_PATH'], subfolder)
        html_path = os.path.join(current_app.config['HTML_PATH'], subfolder)
        filename = title

        upload_markdowns.save(form.markdown.data, folder=subfolder, name=filename + '.md')
        url = os.path.join('article', subfolder, title)

        article = Article(
            title=title,
            category=Category.query.filter_by(id=form.category.data).first(),
            markdown_path=markdown_path,
            html_path=html_path,
            filename=filename,
            add_time=utcnow,
            url=url)
        for t in form.tag.data.split(','):
            tag = Tag.query.filter_by(name=t).first()
            if not tag:
                tag = new_tag(t)
            article.tags.append(tag)

        db.session.add(article)
        db.session.commit()

        flash('Article uploaded.', 'success')

        return redirect(url_for('admin.index'))
    return render_template('admin/upload_article.html', form=form)
