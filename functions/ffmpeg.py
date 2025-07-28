import os
import time
import asyncio
import ffmpeg
from subprocess import check_output
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from config import ENCODE_DIR

def get_codec(filepath, channel="v:0"):
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
        ]
    )
    return output.decode("utf-8").split()


async def encode(filepath):
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
    print(filepath)

    # İkinci ses kanalının kodunu al
    audio_codec = get_codec(filepath, channel='a:1')

    # Ses işleme seçenekleri
    if not audio_codec:
        audio_opts = ['-c:v', 'copy']
    elif audio_codec[0] == 'aac':
        audio_opts = ['-c:v', 'copy', '-c:a', 'copy']
    else:
        audio_opts = ['-c:v', 'copy', '-c:a', 'aac']

    # FFmpeg komutunu oluştur
    command = [
        'ffmpeg',
        '-y',
        '-i', filepath,
        '-map', '0:v:0',    # İlk video kanalı
        '-map', '0:a:1?',   # İkinci ses kanalı (opsiyonel)
        *audio_opts,
        output_filepath
    ]

    # FFmpeg işlemini asenkron olarak çalıştır
    proc = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await proc.communicate()
    return output_filepath


def get_thumbnail(in_filename, path, ttl):
    out_filename = os.path.join(path, str(time.time()) + ".jpg")
    open(out_filename, 'a').close()
    try:
        (
            ffmpeg
                .input(in_filename, ss=ttl)
                .output(out_filename, vframes=1)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
        )
        return out_filename
    except ffmpeg.Error as e:
        return None


def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
        return metadata.get('duration').seconds
    else:
        return 0


def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
        return metadata.get("width"), metadata.get("height")
    else:
        return 1280, 720
