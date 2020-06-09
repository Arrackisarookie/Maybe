#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-25 17:28:37
# @Last modified by:   Arrack
# @Last Modified time: 2020-06-09 14:38:08
#

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from app.extensions import db
from app.models import Base


class ArticleTag(Base):
    __tablename__ = 'article_tag'

    articleID = Column(Integer, ForeignKey('articles.id'), primary_key=True)
    tagID = Column(Integer, ForeignKey('tags.id'), primary_key=True)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    slogan = Column(String(128), default='Everything is not too late.')

    articles = relationship(
        'ArticleTag',
        foreign_keys=[ArticleTag.tagID],
        backref=db.backref('tag', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    @staticmethod
    def exist(self, tagName):
        return Tag.query.filter_by(name=tagName).first() is not None

    def __repr__(self):
        return '<Tag %d-%r>' % (self.id, self.name)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    slogan = Column(String(128), nullable=False)

    articles = relationship('Article', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %d-%r>' % (self.id, self.name)


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)

    title = Column(String(64), nullable=False)
    slogan = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)

    authorID = Column(Integer, ForeignKey('users.id'))
    cateID = Column(Integer, ForeignKey('categories.id'))

    tags = relationship(
        'ArticleTag',
        foreign_keys=[ArticleTag.articleID],
        backref=db.backref('article', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    # replies = relationship('Comment', backref='article', lazy='dynamic')

    def hasTag(self, tag):
        if tag.id is None:
            return False
        return self.tags.filter_by(tagID=tag.id).first() is not None

    def addTag(self, tag):
        if not self.hasTag(tag):
            at = ArticleTag(article=self, tag=tag)
            db.session.add(at)

    def delTag(self, tag):
        at = self.tags.filter_by(tagID=tag.id).first()
        if at:
            db.session.delete(at)

    def __repr__(self):
        return '<Article %d-%r>' % (self.id, self.title)


# class Comment(Base):
#     __tablename__ = 'comments'

#     id = Column(Integer, primary_key=True)
#     type = Column(String(32), nullable=False)

#     content = Column(String(256), nullable=False)

#     authorID = Column(Integer, ForeignKey('users.id'))
#     articleID = Column(Integer, ForeignKey('articles.id'))
#     commentID = Column(Integer, ForeignKey('comments.id'))

#     replies = relationship("Comment", remote_side=[id], backref=db.backref('parent', lazy='dynamic'))

#     def __repr__(self):
#         return '<Comment %d-%r>' % (self.id, self.content)
