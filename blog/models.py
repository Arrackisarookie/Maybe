from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from blog.extensions import db, loginmanager


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(64))

    filename = db.Column(db.String(64))
    html_path = db.Column(db.String(128))
    markdown_path = db.Column(db.String(128))
    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    url = db.Column(db.String(128))

    verified = db.Column(db.Boolean, default=False)
    verified_time = db.Column(db.DateTime, index=True)

    posted = db.Column(db.Boolean, default=False)
    posted_time = db.Column(db.DateTime, index=True)

    cate_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return '<Article %r>' % self.title


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    articles = db.relationship('Article', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.name


class LeaveMsg(db.Model):
    __tablename__ = 'leavemsgs'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<LeaveMsg %r-%r>' % (self.name, self.author)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    leavemsgs = db.relationship('LeaveMsg', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User %r-%r>' % (self.username, self.role)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r permissions=%d>' % (self.name, self.permissions)

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            'User': [
                Permission.LIKE,
                Permission.LEAVEMSG],
            'Writer': [
                Permission.LIKE,
                Permission.LEAVEMSG,
                Permission.WRITE
            ],
            'Moderator': [
                Permission.LIKE,
                Permission.LEAVEMSG,
                Permission.WRITE,
                Permission.MODERATE],
            'Administrator': [
                Permission.LIKE,
                Permission.LEAVEMSG,
                Permission.WRITE,
                Permission.MODERATE,
                Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class Permission(object):
    LIKE = 1
    LEAVEMSG = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


loginmanager.login_view = 'auth.login'
loginmanager.anonymous_user = AnonymousUser
@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
