import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from main import bot
from models import User, db

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("points") & filters.private & ~ filters.forwarded)
async def events(_: Client, msg: Message) -> None:
    points: int = bot.get_user_points(msg.from_user.id)

    with db.session() as session:
        user: User = session.query(User).filter_by(uid=msg.from_user.id).first()

        correct_answer_count: str = str(len([_ for _ in user.answered if _.is_passed]))
        await msg.reply(f"您目前已獲得積分：**{points}** 分\n"
                        f"已解完題目：**{correct_answer_count}** 題")
