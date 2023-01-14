from pyrogram import Client, filters
from config import quee, SUDO_USERS, PRE_LOG
from functions.utils import add_task
from pyrogram.types.bots_and_keyboards import InlineKeyboardButton, InlineKeyboardMarkup
from translation import Translation

video_mimetype = [
    "video/x-flv",
    "video/mp4",
    "video/avi",
    "video/mkv",
    "application/x-mpegURL",
    "video/mp2t",
    "video/3gpp",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-ms-wmv",
    "video/x-matroska",
    "video/webm",
    "video/x-m4v",
    "video/quicktime",
    "video/mpeg"
]


@Client.on_message(filters.user(SUDO_USERS) & filters.incoming & filters.command(['start', 'help']))
async def help_message(app, message):
    await message.reply_text(
        text=Translation.START_TEXT.format(message.from_user.mention()),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Destek", url="https://t.me/botsohbet"
                    )
                ]
            ]
        ),
        reply_to_message_id=message.id
    )


@Client.on_message(filters.user(SUDO_USERS) & filters.incoming & (filters.video | filters.document))
async def encode_video(app, message):
    if message.document:
        if not message.document.mime_type in video_mimetype:
            message.reply_text("```Geçersiz Video !\nBu video dosyasına benzemiyor.```", quote=True)
            return
    await message.reply_text(f"`✔️ Sıraya Eklendi...\nSıra: {len(quee)}\n\nSabırlı olun...\n\n#kuyruk`", quote=True)
    quee.append(message)
    if len(quee) == 1:
        await add_task(app, message) 
