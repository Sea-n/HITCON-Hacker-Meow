from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer

from .database import db


class Answered(db.base):
    __tablename__ = 'answered'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    retry_times = Column(Integer)
    is_passed = Column(Boolean, default=False)

    uid = Column(BigInteger, ForeignKey('users.uid'), nullable=False)
    qid = Column(BigInteger, ForeignKey('questions.qid'), nullable=False)

    def __repr__(self):
        return f"<Answered(user={self.uid}, question={self.qid})>"
