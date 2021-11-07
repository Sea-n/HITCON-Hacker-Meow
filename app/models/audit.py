from sqlalchemy import BigInteger, Column, Integer, JSON

from .database import db


class Audit(db.base):
    __tablename__ = 'audits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(BigInteger, nullable=False)
    item = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<User(uid={self.uid}, item={self.item})>"
