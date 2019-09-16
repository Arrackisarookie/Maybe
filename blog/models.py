from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    posts = db.relationship('Post', backref='category')


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    comments = db.relationship('Comment', backref='post', cascade='all')


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    author = db.Column(db.String(32))
    body = db.Column(db.Text)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replied = db.relationship(          # 被评论的评论
        'Comment', back_populates='replies', remote_side=[id])
    replies = db.relationship(          # 评论的评论
        'Comment', back_populates='replied', cascade='all')
