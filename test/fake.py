#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-27 16:02:25
# @Last modified by:   Arrack
# @Last Modified time: 2020-06-02 12:02:49
#

from faker import Faker

from app.extensions import db
from app.models import Article, Category, Tag, Talk, User, ArticleTag


class Fake(object):
    fake = Faker('zh_CN')

    def cates(self, count=5):
        i = 0
        words = self.fake.words(nb=count, unique=True)
        with db.autoCommit():
            while i < count:
                c = Category(
                    name=words[i],
                    slogan=self.fake.paragraph(nb_sentences=1))
                db.session.add(c)
                i += 1
        return count

    def tags(self, count=5):
        i = 0
        words = self.fake.words(nb=count, unique=True)
        with db.autoCommit():
            while i < count:
                t = Tag(
                    name=words[i],
                    slogan=self.fake.paragraph(nb_sentences=1))
                db.session.add(t)
                i += 1
        return count

    def talks(self, count=50):
        i = 0
        with db.autoCommit():
            while i < count:
                t = Talk(
                    content=self.fake.paragraph(nb_sentences=1),
                    _createTime=self.fake.date_time())
                db.session.add(t)
                i += 1
        return count

    def articles(self, count=10):
        i = 0
        cateCount = Category.query.count()
        tagCount = Tag.query.count()

        with db.autoCommit():
            while i < count:
                a = Article(
                    title=self.fake.sentence(nb_words=7),
                    description=self.fake.paragraph(nb_sentences=5),
                    slogan=self.fake.paragraph(nb_sentences=1),
                    content=self.fake.text(max_nb_chars=1000),
                    category=Category.query.get(self.fake.random_int(min=1, max=cateCount)),
                    # tag=Tag.query.get(self.fake.random_int(min=1, max=tagCount)),
                    author=User.query.get(1),
                    _createTime=self.fake.date_time())
                db.session.add(a)
                for j in range(3):
                    tag = Tag.query.get(j+1)
                    at = ArticleTag(article=a, tag=tag)
                    db.session.add(at)
                i += 1
        return count
