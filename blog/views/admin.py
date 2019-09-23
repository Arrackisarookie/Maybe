import os
import shelve

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import UserMixin, login_user, login_required, logout_user

from blog.config import ADMIN_USERNAME, ADMIN_PASSWORD

from blog import lm, gen
from blog.config import ARTICLE_PATH, BLOG_DAT


bp = Blueprint('admin', __name__, url_prefix='/admin')
user = {
    'username': ADMIN_USERNAME,
    'password': ADMIN_PASSWORD
}


class User(UserMixin):
    pass


class ImportData(object):
    _data = {}
    data_path = BLOG_DAT
    datafile = os.path.join(data_path, 'blog.dat')

    @classmethod
    def _load_data(cls):
        """载入数据"""
        data = shelve.open(cls.datafile)
        for i in data:
            cls._data[i] = data[i]

        return cls._data

    @classmethod
    def get_data(cls):
        """获取数据"""
        if len(cls._data) == 0:
            cls._load_data()

        return cls._data

    @classmethod
    def reload_data(cls):
        """重新载入数据"""
        cls._load_data()


def query_user(username):
    if user['username'] == username:
        return user


@lm.user_loader
def load_user(username):
    if query_user(username) is not None:
        cur_user = User
        cur_user.id = username
        return cur_user
    return None


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        user = query_user(username)
        if user is not None and request.form['password'] == user['password']:
            cur_user = User()
            cur_user.id = username

            login_user(cur_user)

            next = request.args.get('next')
            return redirect(next or url_for('admin.index'))
        flash('Incorrect.')
    return render_template('admin/login.html', title='admin')


@bp.route('/')
@login_required
def index():
    return render_template('admin/admin.html', title='admin-management')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.index'))


@bp.route('/upload/article', methods=['GET', 'POST'])
@login_required
def upload_article():
    source_folder = ARTICLE_PATH
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        path = os.path.join(source_folder, filename)
        file.save(path)

        gen()

        ImportData.reload_data()

        return redirect(url_for('admin.index'))
    return render_template('admin/upload_article.html', title='upload')
