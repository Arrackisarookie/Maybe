from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import login_user, login_required, logout_user

from blog.forms import LoginForm, RegistrationForm
from blog.models import User
from blog.extensions import db


bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Welcome, %s!' % user.username)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('blog.index')
            flash('Welcome, %s!' % user.username)
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('blog.index'))
