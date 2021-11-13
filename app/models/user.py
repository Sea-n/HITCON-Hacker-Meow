from sqlalchemy import BigInteger, Column, Integer
from sqlalchemy.orm import relationship

from .database import db


class User(db.base):
    __tablename__ = 'users'

    uid = Column(BigInteger, primary_key=True)
    points = Column(Integer)

    answered = relationship("Answered", backref="user")

    def __init__(self, uid: int):
        self.uid = uid
        self.points = 0

    def __repr__(self):
        return f"<User(uid={self.uid}, points={self.points})>"
