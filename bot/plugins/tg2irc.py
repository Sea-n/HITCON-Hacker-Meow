import logging
import os
import re

from pyrogram import Client, filters
from pyrogram.types import Message
from typing import List

from main import bot

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.group & ~ filters.edited & ~ filters.service)
async def irc_bridge(_: Client, msg: Message) -> None:
    if str(msg.chat.id) != os.getenv("TELEGRAM_GROUP"):
        return

    p: list = [_ for _ in dir(msg) if
               not _.startswith('_') and
               _ not in (
                   'chat', 'date', 'default', 'forward_date', 'forward_from', 'from_user', 'link', 'media_group_id',
                   'message_id') and
               not getattr(msg, _) in (None, True, False) and
               not hasattr(getattr(msg, _), '__self__')]

    irc_string: str = f"{msg.from_user.first_name}: "

    if "reply_to_message" in p:
        p.remove("reply_to_message")
        if msg.reply_to_message.from_user.is_self:
            pattern = re.compile('^<([^>]+)>: ')
            nick = pattern.search(msg.reply_to_message.text).group(1)
            irc_string += f"{nick}, "
        else:
            irc_string += f"[Reply to {msg.reply_to_message.from_user.first_name}] "

    if "text" in p:
        if msg.text.startswith("/"):
            return

        split_lines: List[str] = msg.text.split("\n", maxsplit=4)

        if len(split_lines) > 1:
            irc_string += f"{split_lines[0]}"
            split_lines[0]: str = irc_string
            send_multilines(split_lines)
            return

        else:
            irc_string += f"{msg.text}"

    else:
        log.debug(p)

        try:
            p.remove("caption")

        except ValueError:
            irc_string += f"A telegram {p[0]}"

        else:
            irc_string += f"A telegram {p[0]} with caption {msg.caption}"

    bot.irc.privmsg(os.getenv("IRC_CHANNEL"), irc_string)


def send_multilines(lines: List[str]):
    empty: str = lines[0].split(':')[0]
    bot.irc.privmsg(os.getenv("IRC_CHANNEL"), lines[0])

    for _ in lines[1:]:
        bot.irc.privmsg(os.getenv("IRC_CHANNEL"), f"{' ' * len(empty)}  {_}")
