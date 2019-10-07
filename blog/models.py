from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from blog.extensions import db, loginmanager


article_tag = db.Table(
    'article_tag',
    db.Column('article_id', db.ForeignKey('articles.id')),
    db.Column('tag_id', db.ForeignKey('tags.id')))


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(64), nullable=False)
    body = db.Column(db.Text, nullable=False)

    add_time = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    url = db.Column(db.String(128), nullable=False, index=True)

    cate_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return '<Article %r>' % self.title


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    articles = db.relationship('Article', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.name


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    articles = db.relationship(
        'Article', secondary=article_tag,
        backref=db.backref('tags', lazy='dynamic'))

    def __repr__(self):
        return '<Tag %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


loginmanager.login_view = 'auth.login'
@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
