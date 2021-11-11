import asyncio
import logging
import os
import platform
import sys
import time
from asyncio import AbstractEventLoop
from datetime import datetime
from signal import SIGABRT, SIGINT, SIGTERM
from typing import Any, Optional, Union

import sqlalchemy
from irc3 import IrcBot
from pyrogram import Client
from pyrogram.errors import ApiIdInvalid, AuthKeyUnregistered
from pyrogram.session import Session
from pyrogram.types import CallbackQuery, Message, User

from bot.random_reply import RandomReply
from models import Audit

log: logging.Logger = logging.getLogger(__name__)


class Bot(RandomReply):
    _instance: Union[None, "Bot"] = None
    me: Optional[User] = None
    app_version: str = os.getenv("VERSION")
    device_model: str = f"PC {platform.architecture()[0]}"
    system_version: str = f"{platform.system()} {platform.python_implementation()} {platform.python_version()}"

    from models import db, Database
    db: Database = db

    if not sqlalchemy.inspect(db.engine).has_table('users'):
        db.init()

    def __init__(self):
        super().__init__()
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
            username=os.getenv("IRC_NICKNAME"), realname=os.getenv("IRC_INFO"),
            sasl_username=os.getenv("IRC_NICKNAME"), sasl_password=os.getenv("IRC_PASSWORD"),
            host='irc.libera.chat', port=6697, ssl=True, debug=True,
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
        loop: AbstractEventLoop = asyncio.get_event_loop()
        run = loop.run_until_complete

        run(self.run_once())

        self.app.plugins = {
            "enabled": True,
            "root": "bot.plugins",
            "include": [],
            "exclude": []
        }
        self.app.start()
        log.debug("[TG] Bot started")
        # self.irc.run(False)
        log.debug("[IRC] Bot started")

        log.debug("Remove registered handlers and register new handlers")

        def handler_int() -> Any:
            log.debug(f"Stop signal received (SIGINT). Exiting...")
            self.irc.notify('SIGINT')
            if getattr(self.irc, 'protocol', None):
                self.irc.quit('INT')
                time.sleep(1)
            # self.irc.loop.stop()

        def handler_term() -> Any:
            log.debug(f"Stop signal received (SIGTERM). Exiting...")

        def handler_abort() -> Any:
            log.debug(f"Stop signal received (SIGABRT). Exiting...")

        if sys.platform != "win32":
            for s in (SIGINT, SIGTERM, SIGABRT):
                loop.remove_signal_handler(s)
            loop.add_signal_handler(SIGINT, handler_int)
            loop.add_signal_handler(SIGTERM, handler_term)
            loop.add_signal_handler(SIGABRT, handler_abort)

            log.debug("Idling...")
            loop.run_forever()

        elif sys.platform == "win32":
            # windows machine doesn't have signal system, raise exception on exit
            log.debug("Idling...")

            try:
                loop.run_forever()

            except KeyboardInterrupt:
                handler_int()

        log.debug("Start stopping tasks")

        self.app.stop()
        log.debug("[TG] Bot stopped")
        self.irc.quit("Client stop successfully")
        log.debug("[IRC] Bot stopped")

    async def run_once(self):
        # Disable notice
        Session.notice_displayed = True
        logging.getLogger("pyrogram").setLevel(logging.WARNING)

        try:
            await self.app.start()

        except (ApiIdInvalid, AttributeError):
            log.critical("[Failed] Api ID is invalid")
            exit(1)

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

        except Exception as e:
            log.exception(e)
            exit(1)

        log.info("Client started successfully")

        await self.app.stop()
        logging.getLogger("pyrogram").setLevel(logging.INFO)

    def audit(self, action: Union[Message, CallbackQuery]) -> None:
        """Audit user incoming actions. For server log usage."""
        log.debug(action)

        audit: Audit = Audit()
        audit.uid = action.from_user.id
        audit.item = action.__str__()

        with self.db.session() as session:
            session.add(audit)
            session.commit()
