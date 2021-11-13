import logging

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from main import bot

log: logging.Logger = logging.getLogger(__name__)


@Client.on_callback_query(filters.all, group=-1)
async def pre_callback(_: Client, callback: CallbackQuery) -> None:
    bot.audit(callback)
