from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.orm import relationship

from .database import db


class Question(db.base):
    __tablename__ = 'questions'

    qid = Column(BigInteger, primary_key=True)
    content = Column(String, nullable=False)
    try_times = Column(Integer, nullable=False)
    points = Column(Integer)

    db_answered = relationship("Answered", backref="question")

    def __repr__(self):
        return f"<Question(id={self.uid}, points={self.points})>"
