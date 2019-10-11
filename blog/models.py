from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from blog.extensions import db, loginmanager


article_tag = db.Table(
    'article_tag',
    db.Column('article_id', db.ForeignKey('articles.id')),
    db.Column('tag_id', db.ForeignKey('tags.id')))


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
        return '{}'.format(self.title)


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    slogan = db.Column(db.String(128), default='Everything is not too late.')
    articles = db.relationship(
        'Article', secondary=article_tag, backref='tags', lazy='dynamic')

    def __repr__(self):
        return '<Tag %r-%d>' % (self.name, self.id)

    def __str__(self):
        return '{}'.format(self.name)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    slogan = db.Column(db.String(128), nullable=False)
    articles = db.relationship('Article', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %r-%d>' % (self.name, self.id)

    def __str__(self):
        return '{}'.format(self.name)


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(64), nullable=False)
    body = db.Column(db.Text, nullable=False)

    add_time = db.Column(db.DateTime, index=True, default=db.func.now())
    update_time = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    isdraft = db.Column(db.Boolean, default=False)

    url = db.Column(db.String(128), index=True, nullable=False)

    cate_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return '<Article %r-%d>' % (self.title, self.id)

    def __str__(self):
        return '{}'.format(self.title)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r-%d>' % (self.username, self.id)

    def __str__(self):
        return '{}'.format(self.username)

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
