import os
import time
import shutil
from config import DOWNLOAD_DIR
from pyrogram.types import Message
from functions.ffmpeg import encode, get_codec, get_thumbnail, get_duration, get_width_height
from functions.progress import progress_for_pyrogram
from pyrogram.errors import FloodWait, MessageNotModified, MessageIdInvalid
from config import quee, PRE_LOG, SUDO_USERS, userbot

async def on_task_complete(app, message: Message):
    del quee[0]
    if len(quee) > 0:
        await add_task(app, quee[0])


async def add_task(app, message: Message):
    try:
        user_id = str(message.from_user.id)
        c_time = time.time()
        random = str(c_time)

        if message.video:
            file_name = message.video.file_name
        elif message.document:
            file_name = message.document.file_name
        elif message.audio:
            file_name = message.audio.file_name
        else:
            file_name = None

        if file_name is None:
            file_name = f"file_{user_id}"

        msg = await message.reply_text("`🟡 Video İşleme Alındı... 🟡\n\n⚙ Motor: Pyrogram\n\n#indirme`", quote=True)
        download_dir = os.path.join(DOWNLOAD_DIR, user_id, random)
        os.makedirs(download_dir, exist_ok=True)
        
        filepath = os.path.join(download_dir, file_name)
        filepath = await message.download(
            file_name=filepath,
            progress=progress_for_pyrogram,
            progress_args=("`İndiriliyor...`", msg, c_time))
        
        await msg.edit("`🟣 Video Kodlanıyor... 🟣\n\n⚙ Motor: FFMPEG\n\n#kodlama`")
        new_file = await encode(filepath)
        
        if not new_file:
            await msg.edit_text("<code>Dosyanızı kodlarken bir şeyler ters gitti.</code>")
            shutil.rmtree(download_dir)
            return
            
        await msg.edit("`🟢 Video Kodlandı, Veriler Alınıyor... 🟢`")
        await handle_upload(app, new_file, message, msg, random, download_dir)
        await msg.edit_text("`✅ Başarıyla Tamamlandı!`")
        
    except MessageNotModified:
        pass
    except MessageIdInvalid:
        await msg.edit_text('❌ İndirme İptal Edildi!')
    except FloodWait as e:
        print(f"⏳ FloodWait için {e.value} saniye bekleme...")
        time.sleep(e.value)
    except Exception as e:
        await msg.edit_text(f"<code>❌ Hata: {str(e)}</code>")
        # Cleanup on error
        if 'download_dir' in locals():
            shutil.rmtree(download_dir, ignore_errors=True)
    finally:
        await on_task_complete(app, message)


async def handle_upload(app, new_file, message, msg, random, base_dir):
    user_id = str(message.from_user.id)
    thumb_image_path = os.path.join(DOWNLOAD_DIR, user_id, f"{user_id}.jpg")
    c_time = time.time()
    
    # Get media metadata
    duration = get_duration(new_file)
    width, height = get_width_height(new_file)
    filename = os.path.basename(new_file)
    audio_codec = get_codec(new_file, channel='a:0')
    file_size = os.path.getsize(new_file)

    # Thumbnail handling
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    else:
        thumb = get_thumbnail(new_file, base_dir, duration / 4)

    # Prepare caption
    caption = message.caption or f"<code>{filename}</code>"
    
    try:
        if file_size > 2_000_000_000:  # 2GB in bytes
            await app.send_message(PRE_LOG, "⚠️ 2GB üstü video geliyor...")
            
            # Upload via userbot
            video = await userbot.send_video(
                chat_id=PRE_LOG,
                video=new_file,
                caption=caption,
                thumb=thumb,
                duration=duration,
                width=width,
                height=height,
                supports_streaming=True,
                progress=progress_for_pyrogram,
                progress_args=("`📤 Log Kanalına Yükleniyor...`", msg, c_time)
            )
            
            # Forward to user
            await app.copy_message(
                chat_id=message.chat.id,
                from_chat_id=PRE_LOG,
                message_id=video.id
            )
        else:
            # Direct upload to user
            await app.send_video(
                chat_id=message.chat.id,
                video=new_file,
                caption=caption,
                thumb=thumb,
                duration=duration,
                width=width,
                height=height,
                supports_streaming=True,
                progress=progress_for_pyrogram,
                progress_args=("`📤 Yükleniyor...`", msg, c_time)
            )
        
        # Audio codec notification
        if not audio_codec:
            await message.reply("`🔇 Bu videonun sesi yoktu ama yine de kodladım.\n\n#bilgilendirme`")
            
    finally:
        # Cleanup temporary files
        try:
            shutil.rmtree(base_dir)
            if thumb != thumb_image_path and os.path.exists(thumb):
                os.remove(thumb)
        except Exception as cleanup_err:
            print(f"❌ Temizleme hatası: {cleanup_err}")
