#
# -*- coding: utf-8 -*-
#
# @adminor: Arrack
# @Date:   2020-05-25 18:22:09
# @Last modified by:   Arrack
# @Last Modified time: 2020-06-02 21:11:51
#

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from app.forms import LoginForm
from app.forms import PostWriteForm
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


@bp.route('/post/write')
@login_required
def postWrite():
    form = PostWriteForm(request.form)
    
    # if request.method == 'POST' and form.validate():

    return render_template('admin/postWrite.html', form=form)


@bp.route('/post/edit')
@login_required
def postEdit(time, name):
    return render_template('admin/postEdit.html')


@bp.route('/setting')
@login_required
def setting():
    return render_template('admin/index.html')


@bp.route('/change-password')
@login_required
def changePassword():
    return render_template('admin/index.html')


@bp.route('/set_site')
@login_required
def set_site():
    return render_template('admin/index.html')


@bp.route('/links')
@login_required
def addLink():
    return render_template('admin/index.html')


@bp.route('/admin-links')
@login_required
def adminLinks():
    return render_template('admin/index.html')


@bp.route('/admin_posts')
@login_required
def admin_posts():
    return render_template('admin/index.html')


@bp.route('/admin_drafts')
@login_required
def admin_drafts():
    return render_template('admin/index.html')


@bp.route('/add_page')
@login_required
def add_page():
    return render_template('admin/index.html')


@bp.route('/admin_pages')
@login_required
def admin_pages():
    return render_template('admin/index.html')


@bp.route('/write_column')
@login_required
def write_column():
    return render_template('admin/index.html')


@bp.route('/admin_columns')
@login_required
def admin_columns():
    return render_template('admin/index.html')


@bp.route('/admin_comments')
@login_required
def admin_comments():
    return render_template('admin/index.html')


@bp.route('/upload_file')
@login_required
def upload_file():
    return render_template('admin/index.html')


@bp.route('/write_shuoshuo')
@login_required
def write_shuoshuo():
    return render_template('admin/index.html')


@bp.route('/add_shuos')
@login_required
def add_shuos():
    return render_template('admin/index.html')


@bp.route('/admin_shuos')
@login_required
def admin_shuos():
    return render_template('admin/index.html')


@bp.route('/add_side_box')
@login_required
def add_side_box():
    return render_template('admin/index.html')


@bp.route('/admin_side_box')
@login_required
def admin_side_box():
    return render_template('admin/index.html')


@bp.route('/qiniu_picbed')
@login_required
def qiniu_picbed():
    return render_template('admin/index.html')
