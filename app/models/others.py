from app.extensions import db


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
