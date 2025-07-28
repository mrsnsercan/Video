import os
import subprocess
import logging
import re
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_audio_tracks(input_video):
    """Videodaki ses sayısını tespit eder"""
    command = [
        'ffprobe', '-v', 'error', '-select_streams', 'a',
        '-show_entries', 'stream=index', '-of', 'csv=p=0', input_video
    ]
    try:
        output = subprocess.check_output(command, text=True, stderr=subprocess.STDOUT)
        return len(output.strip().split('\n')) if output.strip() else 0
    except subprocess.CalledProcessError:
        return 0

def create_audio_keyboard():
    """Ses seçimi için inline klavye oluşturur"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("1. Ses", callback_data="audio_1"),
            InlineKeyboardButton("2. Ses", callback_data="audio_2")
        ],
        [InlineKeyboardButton("Her İkisi", callback_data="audio_both")]
    ])

async def ffmpeg(client, message, input_video, watermark, audio_option=None):
    try:
        # Video metadata al
        cmd = [
            'ffprobe', '-v', 'error', '-show_entries',
            'format=duration:stream=width,height', '-of',
            'csv=p=0', input_video
        ]
        output = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
        width, height, duration = map(float, re.findall(r"[\d.]+", output))
        
        # Watermark boyutlandırma
        watermark_size_percentage = 10
        watermark_resized = "watermark_resized.png"
        resize_cmd = [
            'ffmpeg', '-i', watermark, '-vf',
            f'scale=w=iw*{watermark_size_percentage/100}:h=ow/mdar',
            '-y', watermark_resized
        ]
        subprocess.run(resize_cmd, check=True)

        # Ses seçimi kontrolü
        num_audio = get_audio_tracks(input_video)
        if num_audio == 2 and audio_option is None:
            await message.reply_text(
                "🎧 Videoda 2 ses kanalı bulundu! Lütfen bir seçenek belirtin:",
                reply_markup=create_audio_keyboard()
            )
            return {"status": "audio_choice_required"}

        # Çıkış dosyası adı
        output_video = f"{input_video}.compressed.mp4"
        
        # FFmpeg komutunu oluştur
        command = [
            'ffmpeg', '-i', input_video, '-i', watermark_resized,
            '-filter_complex',
            f'[1][0]scale2ref=w=\'iw*{watermark_size_percentage/100}\':h=\'ow/mdar\'[wm][vid];'
            f'[vid][wm]overlay=main_w-overlay_w-10:main_h-overlay_h-10',
            '-c:v', 'libx264', '-crf', '32', '-preset', 'veryfast'
        ]

        # Ses seçeneklerine göre parametreler
        if audio_option == "audio_1":
            command += ['-map', '0:a:0?', '-c:a', 'copy']
        elif audio_option == "audio_2":
            command += ['-map', '0:a:1?', '-c:a', 'copy']
        elif audio_option == "audio_both":
            command += [
                '-filter_complex', '[0:a:0][0:a:1]amerge=inputs=2[a]',
                '-map', '[a]', '-ac', '2', '-c:a', 'aac'
            ]
        else:  # Varsayılan: ilk sesi kullan
            command += ['-c:a', 'copy']

        command.append(output_video)

        # FFmpeg komutunu çalıştır
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # İlerlemeyi logla
        for line in process.stdout:
            logging.info(line.strip())
        
        # Temizlik
        os.remove(input_video)
        os.remove(watermark_resized)
        
        return {"output": output_video, "duration": duration}

    except Exception as e:
        logging.error(f"FFmpeg error: {str(e)}")
        return {"error": str(e)}
