#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-25 18:11:08
# @Last modified by:   Arrack
# @Last Modified time: 2020-06-11 11:25:18
#

from itsdangerous import BadSignature
from itsdangerous import SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Sericalizer

from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import SmallInteger
from sqlalchemy import String
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import Base


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    default = Column(SmallInteger, default=0)

    users = relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def initRoles():
        roles = ['visitor', 'member', 'admin']
        default_role = 'visitor'

        with db.autoCommit():
            res = []
            for r in roles:
                role = Role.query.filter_by(name=r).first()
                if role is None:
                    role = Role(name=r)
                role.default = 1 if role.name == default_role else 0
                res.append(role)
            db.session.add_all(res)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(64), unique=True, index=True, nullable=False)
    username = Column(String(64), unique=True, nullable=False)
    passwordHash = Column(String(128))

    roleID = Column(Integer, ForeignKey('roles.id'))

    articles = relationship('Article', backref='author', lazy='dynamic')
    # comments = relationship('Comment', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(name='admin').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=1).first()

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.passwordHash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passwordHash, password)

    # todo:
    # change password
    # def generate_reset_token(self, expiration=600):
    #     s = Sericalizer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'reset': self.id}).decode('utf-8')

    # @staticmethod
    # def reset_password(token, new_password):
    #     s = Sericalizer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token.encode('utf-8'))
    #     except SignatureExpired:
    #         return None
    #     except BadSignature:
    #         return None
    #     user = User.query.get(data.get('reset'))
    #     if user is None:
    #         return False
    #     user.password = new_password
    #     db.session.add(user)
    #     return True

    # def generate_auth_token(self, expiration=600):
    #     s = Sericalizer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'id': self.id}).decode('utf-8')

    # @staticmethod
    # def verify_auth_token(token):
    #     s = Sericalizer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return None  # valid token, but expired
    #     except BadSignature:
    #         return None  # invalid token
    #     return User.query.get(data['id'])

    @staticmethod
    def initAdmin(password=None):
        if not password:
            password = input('Initializing Admin, Please set your password:')
        email = current_app.config['ADMIN_EMAIL']
        username = current_app.config['ADMIN_NAME']

        with db.autoCommit():
            admin = User(email=email, username=username, password=password)
            db.session.add(admin)

    def __repr__(self):
        return '<User %d-%r-%r>' % (self.id, self.username, self.role.name)
