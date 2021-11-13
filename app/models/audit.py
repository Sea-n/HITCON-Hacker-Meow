from sqlalchemy import BigInteger, Column, DateTime, Integer, JSON, func

from .database import db


class Audit(db.base):
    __tablename__ = 'audits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(BigInteger, nullable=False)
    time = Column(DateTime(timezone=True), server_default=func.now())
    item = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<Log(uid={self.uid}, item={self.item})>"
