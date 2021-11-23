import logging
from typing import Optional

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

    def get_question_topic(self, qid: str) -> Optional[str]:
        """Get question topic by question id."""
        if self.__is_question_exist(qid):
            with db.session() as session:
                q: Question = session.query(Question).filter_by(qid=qid).first()
                # 可以構造題目字串在此
                return q.topic
        else:
            return None

    def answer_question(self, uid: int, qid: str, answer: str) -> Optional[str]:
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

                user: User = session.query(User).filter_by(uid=uid).first()
                score: str = user.points
                correct_answer_count: str = str(len([_ for _ in user.answered if _.is_passed]))

                if a.is_passed:
                    s: str = f"{q.response}\n" \
                             f"\n" \
                             f"已獲得積分：**{score}** 分\n" \
                             f"已解完題目：**{correct_answer_count}** 題"
                else:
                    s: str = f"哎呀，看起來答案錯誤，再嘗試看看吧！\n" \
                             f"若有任何問題，可以到大會活動組詢問哦！\n" \
                             f"\n" \
                             f"已獲得積分：**{score}** 分\n" \
                             f"已解完題目：**{correct_answer_count}** "

                return s
        return None

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
