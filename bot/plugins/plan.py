import logging

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("plan") & ~ filters.forwarded)
async def plan(cli: Client, msg: Message) -> None:
    keyboard = [[
        InlineKeyboardButton("3 樓", "plan_3F"),
        InlineKeyboardButton("4 樓", "plan_4F"),
    ], [
        InlineKeyboardButton("回主選單", "help"),
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await cli.send_photo(msg.chat.id, "https://i.imgur.com/uQLAd4x.png",
                         "場地總覽\n你想看哪層樓", reply_markup=reply_markup)


@Client.on_callback_query(filters.regex("^plan"))
async def plan_callback(cli: Client, callback: CallbackQuery) -> None:
    if callback.data == "plan":
        keyboard = [[
            InlineKeyboardButton("3 樓", "plan_3F"),
            InlineKeyboardButton("4 樓", "plan_4F"),
        ], [
            InlineKeyboardButton("回主選單", "help"),
        ]]

        media = InputMediaPhoto("https://i.imgur.com/uQLAd4x.png",
                                "場地總覽\n你想看哪層樓")

    elif callback.data == "plan_3F":
        keyboard = [[
            InlineKeyboardButton("R2", "agenda_R2"),
            InlineKeyboardButton("R0", "agenda_R0"),
            InlineKeyboardButton("R3", "agenda_R3"),
        ], [
            InlineKeyboardButton("R2", "agenda_R2"),
            InlineKeyboardButton("R0", "agenda_R0"),
            InlineKeyboardButton("R1", "agenda_R1"),
        ], [
            InlineKeyboardButton("回樓層圖", "plan")
        ]]

        media = InputMediaPhoto("https://i.imgur.com/MqYzHd5.png",
                                "這是 3 樓的平面圖\n對 XX 議程、XX 活動有興趣嗎")

    elif callback.data == "plan_4F":
        keyboard = [[
            InlineKeyboardButton("R4", "agenda_R4"),
        ], [
            InlineKeyboardButton("R0", "agenda_R0"),
        ], [
            InlineKeyboardButton("回樓層圖", "plan")
        ]]

        media = InputMediaPhoto("https://i.imgur.com/y7UcbyJ.png",
                                "這是 4 樓的平面圖\n對 XX 攤位、XX 活動有興趣嗎")

    else:
        log.debug(f"Unknown callback {callback.data}")
        await cli.answer_callback_query(callback.id, f"尚未實作 {callback.data}")
        return

    reply_markup = InlineKeyboardMarkup(keyboard)

    await cli.edit_message_media(callback.message.chat.id,
                                 callback.message.message_id,
                                 media=media, reply_markup=reply_markup)

    await cli.answer_callback_query(callback.id)
