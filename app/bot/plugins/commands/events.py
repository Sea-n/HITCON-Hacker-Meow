import logging

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("events") & filters.private & ~ filters.forwarded)
async def events(cli: Client, msg: Message) -> None:
    keyboard = [[
        InlineKeyboardButton("線上會場 Minetest Venue", "events_minetest"),
        InlineKeyboardButton("線上通訊 Online Chatroom", "events_chatroom")
    ], [
        InlineKeyboardButton("密室逃脫 Virtual Room Escape", "events_room"),
        InlineKeyboardButton("煉蠱大會 Malware Playground", "events_playground")
    ], [
        InlineKeyboardButton("大會代幣 HITCON Token", "events_token"),
        InlineKeyboardButton("限量紀念品", "events_omiyage")
    ], [
        InlineKeyboardButton("回主選單", "help")
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await cli.send_photo(msg.chat.id, "https://i.imgur.com/2bnJbTx.png",
                         "今年大會活動有這些\n請選擇想了解的活動", reply_markup=reply_markup)
