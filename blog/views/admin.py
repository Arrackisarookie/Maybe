from datetime import datetime
import os

from flask import Blueprint, flash, redirect, render_template, url_for, current_app
from flask_login import login_required

from blog import markdowns
from blog.forms import UpdateForm
# from blog.utils import add_meta


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
        data = {}
        data['title'] = form.title.data
        data['category'] = 'test_cate'
        data['tag'] = ['test_tag1', 'test_tag2']

        filename = datetime.now().strftime('%y%m%d%H%M%S' + '.md')

        path = current_app.config['UPLOADED_MARKDOWN_DEST']
        file = os.path.join(path, filename)
        markdowns.save(form.markdown.data, name=filename)

        # add_meta(file, data)
        # gen()

        return redirect(url_for('admin.index'))
    return render_template('admin/upload_article.html', form=form)
