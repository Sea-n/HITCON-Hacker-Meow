import html
import logging
import os

from irc3 import IrcBot, event

from main import bot

log: logging.Logger = logging.getLogger(__name__)


@event('(?P<event>.*)')  # regex
def on_all_events(_: IrcBot, event=None):
    print(event)


@event('^:(?P<nick>\S+)!\S+@\S+ PRIVMSG (?P<channel>#\S+) :(?P<text>.*)')  # regex
def on_new_channel_messages(_: IrcBot, nick=None, channel=None, text=None):
    print(nick, channel, text)
    bot.app.loop.create_task(
        bot.app.send_message(os.getenv("TELEGRAM_GROUP"), f"&lt;{html.escape(nick)}&gt;: {html.escape(text)}")
    )
