import logging

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

log: logging.Logger = logging.getLogger(__name__)


@Client.on_callback_query(filters.all, group=-1)
async def pre_log_callback(cli: Client, callback: CallbackQuery) -> None:
    log.debug(callback.data)
