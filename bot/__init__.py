import logging
import os
import platform
import sys
from datetime import datetime
from typing import Optional, Union

from irc3 import IrcBot
from pyrogram import Client
from pyrogram.errors import ApiIdInvalid, AuthKeyUnregistered
from pyrogram.methods.utilities.idle import idle
from pyrogram.session import Session
from pyrogram.types import User

log: logging.Logger = logging.getLogger(__name__)


class Bot:
    _instance: Union[None, "Bot"] = None
    me: Optional[User] = None
    app_version: str = os.getenv("VERSION")
    device_model: str = f"PC {platform.architecture()[0]}"
    system_version: str = f"{platform.system()} {platform.python_implementation()} {platform.python_version()}"

    def __init__(self):
        self.app: Client = Client(
            "bot",
            app_version=self.app_version,
            device_model=self.device_model,
            api_id=os.getenv("API_ID"),
            api_hash=os.getenv("API_HASH"),
            bot_token=os.getenv("TOKEN"),
            plugins=None,
            system_version=self.system_version
        )

        self.irc: IrcBot = IrcBot.from_config(dict(
            nick=os.getenv("IRC_NICKNAME"), autojoins=[os.getenv("IRC_CHANNEL")],
            username=os.getenv("IRC_INFO"),
            sasl_username=os.getenv("IRC_NICKNAME"), sasl_password=os.getenv("IRC_PASSWORD"),
            host='chat.freenode.net', port=6667, ssl=False, debug=True,
            includes=[
                'irc3.plugins.command',
                'irc3.plugins.logger',
                'bot.irc_plugins.irc2tg',
            ],
        ))

        self.start_time: datetime = datetime.utcnow()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def run(self):
        self.app.run(self.run_once())
        self.app.plugins = {
            "enabled": True,
            "root": "bot.plugins",
            "include": [],
            "exclude": []
        }

        self.app.start()
        self.irc.run(False)

        # TODO: fix exit error
        idle()

        self.app.stop()
        self.irc.quit()

    async def run_once(self):
        # Disable notice
        Session.notice_displayed = True
        logging.getLogger("pyrogram").setLevel(logging.WARNING)

        try:
            await self.app.start()

        except AuthKeyUnregistered:
            log.critical("[Oops!] Session expired!")
            log.critical("        Removed old session and exit...!")
            await self.app.storage.delete()
            exit(1)

        try:
            me: User = await self.app.get_me()

            info_str: str = f"[bot] {me.first_name}"
            info_str += f" {me.last_name}" if me.last_name else ""
            info_str += f" (@{me.username})" if me.username else ""
            info_str += f" ID: {me.id}"
            log.info(info_str)

            self.me: User = me

        except ApiIdInvalid:
            log.critical("[Failed] Api ID is invalid")
            sys.exit(1)

        except Exception as e:
            log.exception(e)
            sys.exit(1)

        log.info("Client started successfully")

        await self.app.stop()
        logging.getLogger("pyrogram").setLevel(logging.INFO)
