import logging

from pyrogram import Client, filters
from pyrogram.types import Message

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.group, group=-1)
async def remove_commands(cli: Client, msg: Message) -> None:
    if msg.text:
        if msg.text.startswith("/"):
            """清除指令"""
            await cli.delete_messages(msg.chat.id, msg.message_id)
        """因為 bot 不需要處理群組訊息，中斷後續指令"""
        msg.stop_propagation()
