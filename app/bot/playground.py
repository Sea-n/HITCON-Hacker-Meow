import logging

from bot.magic_methods import MagicMethods
from models import Answered, Question, User, db

log: logging.Logger = logging.getLogger(__name__)


class Playground(MagicMethods):
    @staticmethod
    def __is_user_answered(uid: int, qid: str) -> bool:
        """Check is user answered the question."""
        with db.session() as session:
            answer: Answered = session.query(Answered).filter_by(qid=qid, uid=uid).first()

            if answer is None:
                answer: Answered = Answered(uid, qid)
                session.add(answer)
                session.commit()
                return False

            if answer.is_passed:
                return True

            return False

    @staticmethod
    def __is_question_exist(qid: str) -> bool:
        """Check question exists."""
        with db.session() as session:
            q: Question = session.query(Question).filter_by(qid=qid).first()

            if q is not None:
                return True
            return False

    def get_question_topic(self, qid: str) -> str:
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

                if self.__is_user_answered(uid, qid):
                    s: str = "你已經完成題目了喔owo\n"

                    s += "恭喜你答對了，但是你已經答對過了，所以沒有分數喔" \
                        if q.answer == answer else \
                        "咦，你不是答對過了嗎"

                    return s

                a: Answered = session.query(Answered).filter_by(qid=qid, uid=uid).first()
                a.retry_times += 1

                if q.answer == answer:
                    a.is_passed = True
                    self.add_user_points(uid, q.points)

                session.add(a)
                session.commit()

                if a.is_passed:
                    s: str = f"恭喜你答對了，你花了 {a.retry_times} 次答對。\n" \
                             f"Response: {q.response}"
                else:
                    s: str = "你答錯了"
                return s
        return self.random_reply()

    @staticmethod
    def init_user(uid: int) -> None:
        """Init user data in db."""
        with db.session() as session:
            user: User = session.query(User).filter_by(uid=uid).first()

            if user is None:
                user: User = User(uid)
                session.add(user)
                session.commit()

    @staticmethod
    def add_user_points(uid: int, points: int) -> None:
        """Add points to user."""
        with db.session() as session:
            user: User = session.query(User).filter_by(uid=uid).first()
            user.points += points

            session.add(user)
            session.commit()

    @staticmethod
    def get_user_points(uid: int) -> int:
        """Get user's current points."""
        with db.session() as session:
            user: User = session.query(User).filter_by(uid=uid).first()
            return user.points

    @staticmethod
    def get_user_answered_list(uid: int) -> list[int]:
        """Get answered question id in list."""
        with db.session() as session:
            user: User = session.query(User).filter_by(uid=uid).first()
            return user.answered
