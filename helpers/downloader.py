import logging
import time
from pathlib import Path
from typing import Dict, Any
from yt_dlp import YoutubeDL

def download_song(
    query: str,
    temp_path: Path,
    config: Dict[str, Any],
    audio_settings: Dict[str, Any]
) -> bool:
    max_retries: int = config.get("max_download_retries", 3)
    retry_delay: int = config.get("retry_delay_seconds", 5)
    audio_format: str = audio_settings.get("format", "mp3").lower()

    output_template = str(temp_path / "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": False,
        "no_warnings": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": audio_format,
            "preferredquality": "0",
        }],
        "default_search": "ytsearch1",
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }
    }

    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"Attempting download: '{query}', attempt {attempt}")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([query])
            return True
        except Exception as e:
            logging.warning(f"Download attempt {attempt} failed for '{query}': {e}")
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                logging.error(f"All {max_retries} download attempts failed for '{query}'")
    return False