from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text

from app.models import Base


class Talk(Base):
    __tablename__ = 'talks'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)

    def __repr__(self):
        return '<Talk %d> content: %r' % (self.id, self.content)
