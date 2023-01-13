import logging
logging.basicConfig(level = logging.DEBUG,
                     format="%(asctime)s - %(name)s - %(message)s - %(levelname)s")

logger = logging.getLogger(__name__)

import pyrogram
import os
from pyrogram import Client
from pyrogram import enums
from config import BOT_TOKEN, APP_ID, API_HASH

logging.getLogger('pyrogram').setLevel(logging.WARNING)


    if not os.path.isdir('downloads'):
        os.mkdir('downloads')
    if not os.path.isdir('encodes'):
        os.mkdir('encodes')

     plugins = dict(root='plugins')

    app = Client(
        'Encoder',
        bot_token=BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    app.run()
    print("Bot Başladı")
