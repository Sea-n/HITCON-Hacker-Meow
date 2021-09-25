import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=str(Path(sys.argv[0]).parent / ".env"), verbose=True)

from bot import Bot

log: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(level=eval(f"logging.{os.getenv('LOG_LEVEL')}"),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.getLogger("pyrogram").setLevel(logging.INFO)

bot: Bot = Bot()

if __name__ == '__main__':
    bot.run()
