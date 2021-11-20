import logging

from pyrogram.types import Message

from models import Reply, db

log: logging.Logger = logging.getLogger(__name__)


class SituationReply:
    def is_situation_exist(self, s: str) -> bool:
        with db.session() as session:
            r: Reply = session.query(Reply).filter_by(situation=s).first()

            if r:
                return True
        return False

    async def situation_reply(self, msg: Message) -> Message:
        with db.session() as session:
            r: Reply = session.query(Reply).filter_by(situation=msg.text).first()

            if r.pic:
                return await msg.reply_photo(r.pic, caption=r.reply)
            return await msg.reply(r.reply)
