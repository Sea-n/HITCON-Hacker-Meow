from sqlalchemy import Column, Integer, String

from .database import db


class Reply(db.base):
    __tablename__ = 'replies'

    rid = Column(Integer, primary_key=True, autoincrement=True)
    reply = Column(String, nullable=False)
    situation = Column(String, nullable=True)
    pic = Column(String, nullable=True)

    def __repr__(self):
        return f"<Reply(id={self.rid}, reply={self.reply})>"
