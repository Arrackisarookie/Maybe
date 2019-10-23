from faker import Faker
from sqlalchemy.exc import IntegrityError

from blog.models.user import User
from blog.extensions import db


def fake_users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(
            email=fake.email(),
            username=fake.user_name(),
            password='1')
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
