#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-25 18:22:09
# @Last modified by:   Arrack
# @Last Modified time: 2020-05-29 11:30:47
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

from app.forms import LoginForm
from app.models import User


bp = Blueprint('auth', __name__)


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
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
