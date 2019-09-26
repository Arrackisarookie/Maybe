from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import login_user, login_required, logout_user

from blog.forms import LoginForm
from blog.models import User


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            login_user(user, remember_me)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('blog.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('blog.index'))
