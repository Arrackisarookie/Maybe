from random import randint

from faker import Faker
from sqlalchemy.exc import IntegrityError

from blog.extensions import db
from blog.models import Admin, Category, Post, Comment


fake = Faker()


def fake_admin():
    admin = Admin(
        username='Administrator',
    )
    admin.set_password('123')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=5):
    category = Category(name='default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=20):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=100):
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # 未审核
        comment = Comment(
            author=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(randint(1, Post.query.count()))
        )
        db.session.add(comment)

    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(randint(1, Comment.query.count())),
            post=Post.query.get(randint(1, Post.query.count()))
        )
        db.session.add(comment)

    db.session.commit()
