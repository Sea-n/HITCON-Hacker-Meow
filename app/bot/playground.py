import logging

from bot.magic_methods import MagicMethods
from models import Answered, Question, db

log: logging.Logger = logging.getLogger(__name__)


class Playground(MagicMethods):
    def is_user_answered(self, uid: int, qid: str) -> bool:
        """Check is user answered the question."""
        with db.session() as session:
            answer: Answered = session.query(Answered).filter_by(qid=qid, uid=uid).first()

            if answer is None:
                answer: Answered = Answered(uid, qid)
                session.add(answer)
                session.commit()
                return True

            if answer.is_passed:
                return True

            return False

    def __is_question_exist(self, qid: str) -> bool:
        """Check question exists."""
        with db.session() as session:
            q: Question = session.query(Question).filter_by(qid=qid).first()

            if q is not None:
                return True
            return False

    def get_question(self, qid: str) -> str:
        """Get question topic by question id."""
        if self.__is_question_exist(qid):
            with db.session() as session:
                q: Question = session.query(Question).filter_by(qid=qid).first()
                # 可以構造題目字串在此
                return q.topic
        else:
            return self.random_reply()

    def answer_question(self, uid: int, qid: str, answer: str) -> str:
        """Try to answer a question by question id and answer."""
        if self.__is_question_exist(qid):
            with db.session() as session:
                q: Question = session.query(Question).filter_by(qid=qid).first()

                if self.is_user_answered(uid, qid):
                    s: str = "你已經完成題目了喔owo"
                    return s

                a: Answered = session.query(Answered).filter_by(qid=qid, uid=uid).first()
                a.retry_times += 1

                if q.answer == answer:
                    a.is_passed = True

                # TODO: add points to user
                session.add(a)
                session.commit()

                if a.is_passed:
                    s: str = f"恭喜你答對了，你花了 {a.retry_times} 次答對。"
                else:
                    s: str = "你答錯了"
                return s
