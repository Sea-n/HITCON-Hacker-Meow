from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import db


class Question(db.base):
    __tablename__ = 'questions'

    qid = Column(Text, primary_key=True)
    level = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    answer = Column(String, nullable=False)

    points = Column(Integer, nullable=False)

    db_answered = relationship("Answered", backref="question")

    def __repr__(self):
        return f"<Question(id={self.qid}, topic={self.topic}, points={self.points})>"
