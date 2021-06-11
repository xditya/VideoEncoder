from telethon import TelegramClient
from decouple import config
import logging
import os

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Basics
api_id = 6
api_hash = "eb06d4abfb49dc3eeb1aeb98ae0f581e"

try:
    bot_token = config("BOT_TOKEN", default=None)
except Exception as e:
    logging.warning(e)
    exit(0)


data = []
download_dir = "downloads/"
if not os.path.isdir(download_dir):
  os.makedirs(download_dir)
  
try:
    BotzHub = TelegramClient("BotzHub", api_id, api_hash).start(bot_token=bot_token)
except Exception as e:
    logging.info(f"Error\n{e}")
    exit(0)
