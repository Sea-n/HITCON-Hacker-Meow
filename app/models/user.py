from sqlalchemy import BigInteger, Column, Integer
from sqlalchemy.orm import relationship

from .database import db


class User(db.base):
    __tablename__ = 'users'

    uid = Column(BigInteger, primary_key=True)
    points = Column(Integer)

    db_answered = relationship("Answered", backref="user")

    def __repr__(self):
        return f"<User(uid={self.uid}, Points={self.points})>"
