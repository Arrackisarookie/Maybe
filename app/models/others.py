from app.extensions import db


class Top(db.Model):
    __tablename__ = 'tops'

    choices = ['article', 'talk', 'leavemsg']

    id = db.Column(db.Integer, primary_key=True)
    foreign_id = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.Enum(*choices), nullable=False)

    def __repr__(self):
        return '<Top %r> %s_id: %d' % (self.type, self.type, self.foreign_id)


class Talk(db.Model):
    __tablename__ = 'talks'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    private = db.Column(db.Boolean, default=False)

    def __repr__(self):
        if self.private:
            return '<Private Talk %d>' % (self.id)
        return '<Talk %d> content: %r' % (self.id, self.content)
