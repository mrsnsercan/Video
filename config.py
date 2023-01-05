import os
from os import environ
from dotenv import load_dotenv

from pyrogram import Client, enums
import logging

logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO
)

LOGGER = logging

if os.path.exists('config.env'):
    load_dotenv('config.env')

quee = []

APP_ID = int(environ.get("APP_ID"))
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")

DOWNLOAD_DIR = environ.get("DOWNLOAD_DIR", "downloads")
ENCODE_DIR = environ.get("ENCODE_DIR", "encodes")
SUDO_USERS = list(set(int(x) for x in environ.get("SUDO_USERS").split()))
PRE_LOG = environ.get("PRE_LOG", "")
STRING_SESSION = environ.get('USER_SESSION_STRING', '')
userbot = Client(name='userbot', api_id=APP_ID, api_hash=API_HASH, session_string=STRING_SESSION, parse_mode=enums.ParseMode.HTML)
userbot.start()
print("Userbot Başlatıldı 4 gb yükleme aktif")
