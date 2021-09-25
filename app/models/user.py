from sqlalchemy import BigInteger, Column, String

from .database import db


class User(db.base):
    __tablename__ = 'users'

    uid = Column(BigInteger, primary_key=True)
    jwt_token = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(uid={self.uid}, token={self.jwt_token})>"
