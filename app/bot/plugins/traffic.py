import logging

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message

log: logging.Logger = logging.getLogger(__name__)

GMAP_LINK: str = "https://goo.gl/maps/zDB1HgoGKMb9nCVG6"
EVENT_ADDRESS: str = "中央研究院 人文社會科學館\n\n台北市南港區研究院路二段 128 號"


@Client.on_message(filters.command("traffic") & ~ filters.forwarded)
async def traffic(cli: Client, msg: Message) -> None:
    keyboard = [[
        InlineKeyboardButton("捷運", "traffic_mrt"),
        InlineKeyboardButton("台鐵 / 高鐵", "traffic_tra"),
        InlineKeyboardButton("公車", "traffic_bus"),
    ], [
        InlineKeyboardButton("自行開車", "traffic_car"),
        InlineKeyboardButton("Google 地圖", url=GMAP_LINK),
    ], [
        InlineKeyboardButton("回主選單", "help")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await cli.send_photo(msg.chat.id, "https://i.imgur.com/t19xHxU.png",
                         EVENT_ADDRESS, reply_markup=reply_markup)


@Client.on_callback_query(filters.regex('^traffic'), group=1)
async def traffic_callback(cli: Client, callback: CallbackQuery) -> None:
    # 不知道誰註冊掉 traffic 了，只好讓他在 group 1
    keyboard = [[
        InlineKeyboardButton("回交通方式", "traffic")
    ]]

    if callback.data == "traffic":
        keyboard = [[
            InlineKeyboardButton("捷運", "traffic_mrt"),
            InlineKeyboardButton("台鐵 / 高鐵", "traffic_tra"),
            InlineKeyboardButton("公車", "traffic_bus"),
        ], [
            InlineKeyboardButton("自行開車", "traffic_car"),
            InlineKeyboardButton("Google 地圖", url=GMAP_LINK),
        ], [
            InlineKeyboardButton("回主選單", "help")
        ]]

        media = InputMediaPhoto("https://i.imgur.com/t19xHxU.png",
                                EVENT_ADDRESS)

    elif callback.data == "traffic_mrt":
        media = InputMediaPhoto("https://i.imgur.com/PCAgSF7.png",
                                "搭捷運板南線至南港站（1 號出口）換乘公車 212（直行/區間）、270 或藍 25 至中研院站\n"
                                "搭捷運文湖線至南港展覽館站（2 號出口），走至南港國小對面換乘公車 205、276、306 或 645 至中研院站")

    elif callback.data == "traffic_tra":
        media = InputMediaPhoto("https://i.imgur.com/PCAgSF7.png",
                                "至「南港站」換乘公車 212、270 或藍 25（中研院站）")

    elif callback.data == "traffic_bus":
        media = InputMediaPhoto("https://i.imgur.com/FmMu5j2.png",
                                "205、212（直行/區間）、270、276、306、620、645（中研院站，前一站為中研新村站）")

    elif callback.data == "traffic_car":
        media = InputMediaPhoto("https://i.imgur.com/QNzEtiy.png",
                                "CAR")

    else:
        log.debug(f"Unknown callback {callback.data}")
        await cli.answer_callback_query(callback.id, f"尚未實作 {callback.data}")
        return

    await cli.edit_message_media(callback.message.chat.id,
                                 callback.message.message_id,
                                 media=media,
                                 reply_markup=InlineKeyboardMarkup(keyboard))

    await cli.answer_callback_query(callback.id)
