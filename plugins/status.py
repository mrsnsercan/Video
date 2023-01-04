import shutil
import psutil
import math

from functions.progress import humanbytes
from config import quee
from pyrogram import Client, filters


@Client.on_message(filters.command("status"))
async def status(app, message):
    msg = await message.reply_text(text="`Bekle 😊😇🙃`")
    toplam, kullanilan, bos = shutil.disk_usage(".")
    toplam = humanbytes(toplam)
    kullanilan = humanbytes(kullanilan)
    bos = humanbytes(bos)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    text = f"**Toplam Alanım:** `{toplam}` \n"
    text += f"**Kullanılan Alan:** `{kullanilan}({disk_usage}%)` \n"
    text += f"**Boş Alanım:** `{bos}` \n"
    text += f"**CPU Kullanımım:** `{cpu_usage}%` \n"
    text += f"**RAM Kullanımım:** `{ram_usage}%`\n\n"
    text += f"**Ayrıca Yapacak {len(quee)} işim var 😡**" 
    await msg.edit(
        text=text
    )
    return
