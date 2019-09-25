from datetime import datetime
import os

from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import UserMixin, login_user, login_required, logout_user

from blog import gen, markdowns
from blog.forms import LoginForm, UpdateForm
from blog.utils import add_meta


bp = Blueprint('admin', __name__)
# user = {
#     'username': current_app.config['ADMIN_USERNAME'],
#     'password': current_app.config['ADMIN_PASSWORD']
# }


# class User(UserMixin):
#     pass


# def query_user(username):
#     if user['username'] == username:
#         return user


# @bp.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         username = form.username.data
#         password = form.password.data
#         user = query_user(username)
#         if user is not None and password == user['password']:
#             cur_user = User()
#             cur_user.id = username

#             login_user(cur_user)

#             next = request.args.get('next')
#             return redirect(next or url_for('admin.index'))
#         flash('Incorrect.')
#     return render_template('admin/login.html', form=form)


@bp.route('/')
# @login_required
def index():
    return render_template('admin/admin.html', title='admin-management')


@bp.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('admin.index'))


@bp.route('/upload/article', methods=['GET', 'POST'])
# @login_required
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

        add_meta(file, data)
        # gen()

        return redirect(url_for('admin.index'))
    return render_template('admin/upload_article.html', form=form)
