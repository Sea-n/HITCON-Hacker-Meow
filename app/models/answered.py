from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, Text

from .database import db


class Answered(db.base):
    __tablename__ = 'answered'

    id = Column(Integer, primary_key=True, autoincrement=True)
    retry_times = Column(Integer)
    is_passed = Column(Boolean, default=False)

    uid = Column(BigInteger, ForeignKey('users.uid'), nullable=False)
    qid = Column(Text, ForeignKey('questions.qid'), nullable=False)

    def __init__(self, uid: int, qid: str):
        self.uid = uid
        self.qid = qid
        self.retry_times = 0
        self.is_passed = False

    def __repr__(self):
        return f"<Answered(user={self.uid}, question={self.qid})>"
