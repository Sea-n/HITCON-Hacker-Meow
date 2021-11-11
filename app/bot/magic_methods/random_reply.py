import logging
import random

import requests

log: logging.Logger = logging.getLogger(__name__)
CONTENT_URL: str = "https://raw.githubusercontent.com/Sea-n/HITCON-Hacker-Meow/master/app/content.txt"


class RandomReply:
    _reply_list: list = list()

    def update_random_reply_list(self) -> None:
        _r: requests = requests.get(CONTENT_URL)
        if _r.status_code != 200:
            raise ConnectionError("Can not get the content, is the bot in offline mode?")

        for w in _r.text.split(",\n"):
            if w:
                self._reply_list.append(w)

    def random_reply(self) -> str:
        if not self._reply_list:
            self.update_random_reply_list()
        random_str: str = random.choice(self._reply_list)
        return random_str
