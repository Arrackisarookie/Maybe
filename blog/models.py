from datetime import date
import re

from itsdangerous import (
    TimedJSONWebSignatureSerializer as Sericalizer,
    BadSignature, SignatureExpired
)
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db, loginmanager
from .utils import Translator


article_tag = db.Table(
    'article_tag',
    db.Column('article_id', db.ForeignKey('articles.id')),
    db.Column('tag_id', db.ForeignKey('tags.id')))


class Top(db.Model):
    __tablename__ = 'tops'

    choices = ['article', 'talk', 'leavemsg']

    id = db.Column(db.Integer, primary_key=True)
    foreign_id = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.Enum(*choices), nullable=False)

    def __repr__(self):
        return '<Top %r> %s_id: %d' % (self.type, self.type, self.foreign_id)

    def __str__(self):
        return 'Top %s, %s_id: %d' % (self.type, self.type, self.foreign_id)

    def to_json(self):
        json_top = {
            'id': self.id,
            'type': self.content,
            'foreign_id': self.foreign_id
        }
        return json_top


class Talk(db.Model):
    __tablename__ = 'talks'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    add_time = db.Column(db.DateTime, index=True, default=db.func.now())
    private = db.Column(db.Boolean, default=False)

    def __repr__(self):
        if self.private:
            return '<Talk %d> Private.' % (self.id)
        return '<Talk %d> content: %r' % (self.id, self.content)

    def __str__(self):
        if self.private:
            return 'Talk %d is set to be private.' % (self.id)
        return 'Talk %d: %s' % (self.id, self.content)

    def to_json(self):
        json_talk = {
            'id': self.id,
            'content': self.content,
            'private': self.private
        }
        return json_talk


class About(db.Model):
    __tablename__ = 'abouts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    slogan = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text, nullable=False)
    add_time = db.Column(db.DateTime, index=True, default=db.func.now())
    update_time = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    url = db.Column(db.String(128))

    def __repr__(self):
        return '<About %r>' % self.title

    def __str__(self):
        return 'About %s' % (self.title)

    def to_json(self):
        json_about = {
            'id': self.id,
            'title': self.name,
            'slogan': self.slogan,
            'body': self.body,
            'add_time': self.add_time,
            'update_time': self.update_time,
            'url': self.url
        }
        return json_about


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    slogan = db.Column(db.String(128), default='Everything is not too late.')
    articles = db.relationship(
        'Article', secondary=article_tag, backref='tags', lazy='dynamic')

    def __repr__(self):
        return '<Tag %d-%r>' % (self.id, self.name)

    def __str__(self):
        return 'Tag %d-%s' % (self.id, self.name)

    def to_json(self):
        json_tag = {
            'id': self.id,
            'name': self.name,
            'slogan': self.slogan
        }
        return json_tag


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    slogan = db.Column(db.String(128), nullable=False)
    articles = db.relationship('Article', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %d-%r>' % (self.id, self.name)

    def __str__(self):
        return 'Category %d-%s' % (self.id, self.name)

    def to_json(self):
        json_cate = {
            'id': self.id,
            'name': self.name,
            'slogan': self.slogan
        }
        return json_cate


def default_name(context):
    title = context.get_current_parameters()['title']
    translator = Translator()

    words = re.findall(r'[a-z0-9A-Z]+', translator.translate(title))
    return '-'.join(words)


def default_url(context):
    name = context.get_current_parameters()['name']
    today = date.today()
    return '/'.join(['/article', str(today.year), str(today.month), name])


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), default=default_name, onupdate=default_name, nullable=False, unique=True)
    url = db.Column(db.String(128), default=default_url, onupdate=default_url, nullable=False, unique=True)

    body = db.Column(db.Text, nullable=False)
    add_time = db.Column(db.DateTime, index=True, default=db.func.now())

    update_time = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # can remove ?
    isdraft = db.Column(db.Boolean, default=False)

    cate_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return '<Article %d-%r>' % (self.id, self.title)

    def __str__(self):
        return 'Artile %d-%s' % (self.id, self.title)

    def to_json(self):
        json_article = {
            'id': self.id,
            'body': self.body,
            'title': self.title,
            'add_time': self.add_time,
            'update_time': self.update_time,
            'isdraft': self.isdraft,
            'url': self.url,
            # 'category': Category.query.get(int(self.cate_id)).name
            # 'tag': Tag.query.filter_by()
        }
        return json_article


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User %d-%r>' % (self.id, self.username)

    def __str__(self):
        return 'User %d-%s' % (self.id, self.username)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Sericalizer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Sericalizer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        return User.query.get(data['id'])

    def to_json(self):
        json_user = {
            'id': self.id,
            'username': self.username,
        }
        return json_user


loginmanager.login_view = 'auth.login'
@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
