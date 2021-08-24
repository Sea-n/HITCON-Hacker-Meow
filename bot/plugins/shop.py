import logging

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("shop") & ~ filters.forwarded)
async def shop(cli: Client, msg: Message) -> None:
    keyboard = [[
        InlineKeyboardButton("T-Shirt", "shop_shirt"),
        InlineKeyboardButton("電路板", "shop_board"),
    ], [
        InlineKeyboardButton("背包", "shop_pack"),
        InlineKeyboardButton("紀念小物", "shop_others"),
        InlineKeyboardButton("限定推薦", "shop_recommended"),
    ], [
        InlineKeyboardButton("回主選單", "help"),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await cli.send_photo(msg.chat.id, "https://i.imgur.com/054ENew.png",
                         "歡迎來到 *HITCON 線上商城*\n\n"
                         "使用者：*Hacker Meow* (金級贊助商)\n"
                         "點數：*4,200 點*\n\n"
                         "請告訴駭客喵喵你想逛哪個分類", reply_markup=reply_markup)


@Client.on_callback_query(filters.regex('^shop'))
async def shop_callback(cli: Client, callback: CallbackQuery) -> None:
    keyboard = [[
        InlineKeyboardButton("回 HITCON 商城", "shop")
    ]]

    if callback.data == "shop":
        keyboard = [[
            InlineKeyboardButton("T-Shirt", "shop_shirt"),
            InlineKeyboardButton("電路板", "shop_board"),
        ], [
            InlineKeyboardButton("背包", "shop_pack"),
            InlineKeyboardButton("紀念小物", "shop_others"),
            InlineKeyboardButton("限定推薦", "shop_recommended"),
        ], [
            InlineKeyboardButton("回主選單", "help"),
        ]]

        media = InputMediaPhoto("https://i.imgur.com/054ENew.png",
                                "歡迎來到 *HITCON 線上商城*\n\n"
                                "使用者：*Hacker Meow* (金級贊助商)\n"
                                "點數：*4,200 點*\n\n"
                                "請告訴駭客喵喵你想逛哪個分類")

    elif callback.data == "shop_shirt":
        keyboard = [[
            InlineKeyboardButton("DEFENSE 2019", "shop_shirt_def19"),
            InlineKeyboardButton("CMT 2018", "shop_shirt_cmt18"),
        ], [
            InlineKeyboardButton("Pacific 2018", "shop_shirt_pac19"),
            InlineKeyboardButton("HITCON 2021", "shop_shirt_conf21"),
        ], [
            InlineKeyboardButton("⬅️ 限定推薦", "shop_recommended"),
            InlineKeyboardButton("回線上商城", "shop"),
            InlineKeyboardButton("電路板 ➡️", "shop_board"),
        ]]

        media = InputMediaPhoto("https://i.imgur.com/SvfPYmi.png",
                                "HITCON 線上商城 > *T-shirt*\n\n"
                                "短袖 T-Shirt 搭配印花設計，實用及紀念性兼具之必收藏單品！")

    elif callback.data == "shop_shirt_def19":
        keyboard = [[
            InlineKeyboardButton("開啟 HITCON 線上商城", url="https://t.me/"),
            InlineKeyboardButton("參考蝦皮賣場", url="https://t.me/"),
        ], [
            InlineKeyboardButton("⬅️ DEFENSE 2018 連帽外套", "shop_shirt_def18"),
            InlineKeyboardButton("HITCON 2021 T-Shirt ➡️", "shop_shirt_conf21"),
        ], [
            InlineKeyboardButton("回 T-shirt 分類", "shop_shirt"),
        ]]

        media = InputMediaPhoto("https://i.imgur.com/Y4RBIwc.png",
                                "HITCON 線上商城 > T-shirt > *HITCON DEFENSE 2019 連帽外套*\n\n"
                                "附兩側口袋、帽繩、拉鍊，採低調深藍色設計，小巧精緻的電繡 Logo ，穿起來簡約時尚，上班、出遊、約會穿都好看，為駭客年度必備單品，就算你不是駭客，也值得擁有！\n\n"
                                "價格：2,500 點 / $1,500 NTD\n庫存數量：80")

    else:
        log.debug(f"Unknown callback {callback.data}")
        await cli.answer_callback_query(callback.id, f"尚未實作 {callback.data}")
        return

    await cli.edit_message_media(callback.message.chat.id,
                                 callback.message.message_id,
                                 media=media,
                                 reply_markup=InlineKeyboardMarkup(keyboard))

    await cli.answer_callback_query(callback.id)
