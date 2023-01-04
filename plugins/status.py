import shutil
import psutil
import math

from functions.progress import humanbytes
from config import quee
from pyrogram import Client, filters


@Client.on_message(filters.command("status"))
async def status(app, message):
    msg = await m.reply_text(text="`Bekle 😊😇🙃`")
    toplam, kullanilan, bos = shutil.disk_usage(".")
    toplam = humanbytes(toplam)
    kullanilan = humanbytes(kullanilan)
    bos = humanbytes(bos)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    text = f"**Toplam Disk Alanı:** `{toplam}` \n"
    text += f"**Kullanılan Alan:** `{kullanilan}({disk_usage}%)` \n"
    text += f"**Boş Alan:** `{bos}` \n"
    text += f"**CPU Kullanımı:** `{cpu_usage}%` \n"
    text += f"**RAM Kullanımı:** `{ram_usage}%`\n\n"
    text += f"**Yapacak {len(quee)} işim var.**" 
