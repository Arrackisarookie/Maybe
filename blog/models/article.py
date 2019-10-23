from datetime import date
import re

from .extensions import db
from .utils import Translator


article_tag = db.Table(
    'article_tag',
    db.Column('article_id', db.ForeignKey('articles.id')),
    db.Column('tag_id', db.ForeignKey('tags.id')))


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
    # 草稿独自整一个表
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), default=default_name, onupdate=default_name, nullable=False, unique=True)
    url = db.Column(db.String(128), default=default_url, onupdate=default_url, nullable=False, unique=True)

    body = db.Column(db.Text, nullable=False)
    add_time = db.Column(db.DateTime, index=True, default=db.func.now())

    update_time = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

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
