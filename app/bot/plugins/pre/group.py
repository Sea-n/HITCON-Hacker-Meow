import logging

from pyrogram import Client, filters
from pyrogram.types import Message

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.group, group=-1)
async def remove_commands(cli: Client, msg: Message) -> None:
    if msg.text:
        """檢查訊息存在"""
        if msg.text.startswith("/"):
            """清除指令"""
            await cli.delete_messages(msg.chat.id, msg.message_id)
