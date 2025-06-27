import subprocess
import logging
import time


def download_song(query, temp_file_path, config, audio_settings):
    max_retries = config.get("max_download_retries", 3)
    retry_delay = config.get("retry_delay_seconds", 5)
    audio_format = audio_settings.get("format", "mp3").lower()

    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", audio_format,
        "--audio-quality", "0",
        "-f", "bestaudio/best",
        "-o", temp_file_path.as_posix(),
        f"ytsearch1:{query}"
    ]

    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"Attempting download: '{query}', attempt {attempt}")
            logging.debug(f"Download command: {' '.join(command)}")
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, text=True)
            return True
        except subprocess.CalledProcessError as e:
            logging.warning(f"Download attempt {attempt} failed for '{query}': {e}")
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                logging.error(f"All {max_retries} download attempts failed for '{query}'")
    return False