from datetime import datetime
import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import UserMixin, login_user, login_required, logout_user

from blog.config import ADMIN_USERNAME, ADMIN_PASSWORD

from blog import gen
from blog.config import ARTICLE_PATH


ALLOWED_EXTENSIONS = {'.md'}

bp = Blueprint('admin', __name__, url_prefix='/admin')
user = {
    'username': ADMIN_USERNAME,
    'password': ADMIN_PASSWORD
}


class User(UserMixin):
    pass


def query_user(username):
    if user['username'] == username:
        return user


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
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part.')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file.')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            filename = datetime.now().strftime('%y%m%d%H%M%S' + '.md')
            path = os.path.join(source_folder, filename)
            file.save(path)
        else:
            flash('Incorrect file type, need .md')

        gen()

        return redirect(url_for('admin.index'))
    return render_template('admin/upload_article.html', title='upload')


def allowed_file(filename):

    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS
