import logging
import random

from pyrogram.types import Message

from models import Reply, db

log: logging.Logger = logging.getLogger(__name__)


class RandomReply:
    async def random_reply(self, msg: Message) -> Message:
        with db.session() as session:
            r: list[Reply] = session.query(Reply).filter_by(situation=None).all()
            random_choice: Reply = random.choice(r)

            if random_choice.pic is not None:
                return await msg.reply_photo(random_choice.pic, caption=random_choice.reply)
            return await msg.reply(random_choice.reply)
