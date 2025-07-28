import os
import time
import asyncio
import ffmpeg
from subprocess import check_output, CalledProcessError
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from config import ENCODE_DIR

def get_codec(filepath, channel="v:0"):
    try:
        output = check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                channel,
                "-show_entries",
                "stream=codec_name,codec_tag_string",
                "-of",
                "default=nokey=1:noprint_wrappers=1",
                filepath,
            ],
            stderr=asyncio.subprocess.PIPE
        )
        return output.decode("utf-8").split()
    except CalledProcessError as e:
        print(f"ffprobe error: {e.stderr.decode() if e.stderr else str(e)}")
        return None


async def encode(self, filepath):
    path, extension = os.path.splitext(filepath)
    file_name = os.path.basename(path)
    encode_dir = os.path.join(
        ENCODE_DIR,
        file_name
    )
    output_filepath = encode_dir + '.mp4'
    assert (output_filepath != filepath)
    if os.path.isfile(output_filepath):
        print('"{}" Atlanıyor: dosya zaten var'.format(output_filepath))
        return output_filepath
    print(f"Encoding: {filepath}")

    # Ses kanalını güvenli şekilde kontrol et
    audio_codec = get_codec(filepath, channel='a:0')

    # FFmpeg komutunu oluştur
    command = [
        'ffmpeg',
        '-y',
        '-i', filepath,
        '-map', '0:v:0',    # İlk video kanalı
        '-c:v', 'copy',     # Videoyu her durumda kopyala
    ]

    # Ses kanalı varsa ve AAC değilse dönüştür, AAC ise kopyala
    if audio_codec:
        if audio_codec[0] != 'aac':
            command.extend(['-map', '0:a:0?', '-c:a', 'aac'])
        else:
            command.extend(['-map', '0:a:0?', '-c:a', 'copy'])
    else:
        print("⚠️ Ses kanalı bulunamadı, sadece video kopyalanacak")

    command.append(output_filepath)

    # FFmpeg işlemini asenkron olarak çalıştır
    proc = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        print(f"❌ FFmpeg hatası: {stderr.decode()}")
    else:
        print(f"✅ Başarıyla kodlandı: {output_filepath}")
    
    return output_filepath


def get_thumbnail(in_filename, path, ttl):
    # Çıktı dosya adını oluştur
    out_filename = os.path.join(path, f"thumbnail_{int(time.time())}.jpg")
    
    try:
        # Önce dosyayı oluştur (eğer ffmpeg başarısız olursa, bu dosyayı sileceğiz)
        open(out_filename, 'w').close()
        
        # Thumbnail oluştur
        (
            ffmpeg
            .input(in_filename, ss=ttl)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return out_filename
    except ffmpeg.Error as e:
        # Hata oluştu, oluşturduğumuz dosyayı silelim
        if os.path.exists(out_filename):
            os.remove(out_filename)
        print(f"Thumbnail oluşturma hatası: {e.stderr.decode() if e.stderr else str(e)}")
        return None
    except Exception as e:
        # Diğer hatalar
        if os.path.exists(out_filename):
            os.remove(out_filename)
        print(f"Beklenmeyen hata: {str(e)}")
        return None


def get_duration(filepath):
    try:
        metadata = extractMetadata(createParser(filepath))
        if metadata and metadata.has("duration"):
            return metadata.get('duration').seconds
    except Exception as e:
        print(f"Süre alma hatası: {str(e)}")
    return 0


def get_width_height(filepath):
    try:
        metadata = extractMetadata(createParser(filepath))
        if metadata and metadata.has("width") and metadata.has("height"):
            return metadata.get("width"), metadata.get("height")
    except Exception as e:
        print(f"Çözünürlük alma hatası: {str(e)}")
    return 1280, 720
