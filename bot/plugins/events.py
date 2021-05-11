import logging

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import CallbackQuery, InputMediaPhoto

log: logging.Logger = logging.getLogger(__name__)


@Client.on_message(filters.command("events") & ~filters.forwarded)
async def events(cli: Client, msg: Message) -> None:
    keyboard = [[InlineKeyboardButton("線上會場 Minetest Venue", "events_minetest"),
                 InlineKeyboardButton("線上通訊 Online Chatroom", "events_chatroom")],
                [InlineKeyboardButton("密室逃脫 Virtual Room Escape", "events_room"),
                 InlineKeyboardButton("煉蠱大會 Malware Playground", "events_playground")],
                [InlineKeyboardButton("大會代幣 HITCON Token", "events_token"),
                 InlineKeyboardButton("限量紀念品", "events_omiyage")],
                [InlineKeyboardButton("回主選單", "help")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await cli.send_photo(msg.chat.id, "https://i.imgur.com/2bnJbTx.png",
                         "今年大會活動有這些\n請選擇想了解的活動", reply_markup=reply_markup)


@Client.on_callback_query(filters.regex('^events'))
async def events_callback(cli: Client, callback: CallbackQuery) -> None:
    if callback.data == "events":
        buttons = [{
            "線上會場 Minetest Venue": "events_minetest",
            "線上通訊 Online Chatroom": "events_chatroom",
            "密室逃脫 Virtual Room Escape": "events_room"
        }, {
            "煉蠱大會 Malware Playground": "events_playground",
            "大會代幣 HITCON Token": "events_token",
            "限量紀念品": "events_omiyage"
        }, {
            "回主選單": "help"
        }]

        media = InputMediaPhoto("https://i.imgur.com/2bnJbTx.png",
                                "今年大會活動有這些\n請選擇想了解的活動")

    elif callback.data == "events_minetest":
        buttons = [{
            "說明文件": "https://hackmd.io/5-6iCtYFSS6smJxE2fVhrQ"
        }, {
            "回活動總覽": "events"
        }]

        media = InputMediaPhoto("https://i.imgur.com/aefywRO.png",
                                "此次線上虛擬會場使用 Minetest 架設。這是一個類似 Minecraft 的 自由軟體 沙盒遊戲。\n\n由於該遊戲本體不支援中文輸入，您可以選擇使用僅限英文輸入但有支援各平台的 Minetest 官方版本，或是選擇虛擬會場說明文件中的由大會方進行 patch 的中文輸入版本。操作說明可參照 Minetest 官方說明。")

    elif callback.data == "events_playground":
        buttons = [{
            "說明文件": "https://hackmd.io/YoOBx8AxSuuA3uzM7jo3kA"
        }, {
            "新手村計分板": "http://r1.hitcon20mpg.tw:8081/",
            "進階場計分板": "http://example.com/"
        }, {
            "回活動總覽": "events"
        }]

        media = InputMediaPhoto("https://i.imgur.com/XDVEZrj.png",
                                "玩家可以透過Raw TCP Socket連上煉蠱伺服器。遊戲共有兩個Port，一個用於下指令（以下簡稱指令Port），另一個用於觀看目前狀況。（以下簡稱狀況Port）\n\n指令Port只能用來輸入指令，他不會回傳給你任何資料。輸入指令的回傳資料會顯示在狀況Port，因此建議同時開兩個視窗然後同時看兩者。")

    else:
        log.debug(f"Unknown callback {callback.data}")
        await cli.answer_callback_query(callback.id, f"尚未實作 {callback.data}")
        return

    keyboard = []
    for k in buttons:
        row = []
        for txt in k:
            if 'https://' in k[txt]:
                button = InlineKeyboardButton(text=txt, url=k[txt])
            else:
                button = InlineKeyboardButton(text=txt, callback_data=k[txt])
            row.append(button)
        keyboard.append(row)

    await cli.edit_message_media(callback.message.chat.id,
                                 callback.message.message_id,
                                 media=media,
                                 reply_markup=InlineKeyboardMarkup(keyboard))

    await cli.answer_callback_query(callback.id)
