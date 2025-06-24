import subprocess
import logging
import time

def download_song(query, temp_path, config, audio_settings):
    max_retries = config.get("max_download_retries", 3)
    retry_delay = config.get("retry_delay_seconds", 5)
    audio_format = audio_settings.get("format", "mp3")

    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", audio_format,
        "-o", temp_path.as_posix(),
        f"ytsearch1:{query}"
    ]

    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"Attempting download: '{query}', attempt {attempt}")
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError as e:
            logging.warning(f"Download attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(retry_delay)
    return False
