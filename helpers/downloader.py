import subprocess
import logging
import time
from pathlib import Path
from typing import Dict, Any

def download_song(
    query: str,
    temp_path: Path,
    config: Dict[str, Any],
    audio_settings: Dict[str, Any]
) -> bool:
    max_retries: int = config.get("max_download_retries", 3)
    retry_delay: int = config.get("retry_delay_seconds", 5)
    audio_format: str = audio_settings.get("format", "mp3").lower()
    command: list[str] = [
        "yt-dlp", "--extract-audio",
        "--audio-format", audio_format,
        "--audio-quality", "0",
        "-f", "bestaudio/best",
        "-o", temp_path.as_posix(),
        f"ytsearch1:{query}"
    ]
    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"Attempting download: '{query}', attempt {attempt}")
            logging.debug(f"Running command: {' '.join(command)}")
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            logging.debug(f"yt-dlp stdout: {result.stdout}")
            logging.debug(f"yt-dlp stderr: {result.stderr}")
            return True
        except subprocess.CalledProcessError as e:
            logging.warning(f"Download attempt {attempt} failed for '{query}': {e}")
            logging.error(f"yt-dlp stdout: {e.stdout}")
            logging.error(f"yt-dlp stderr: {e.stderr}")
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                logging.error(f"All {max_retries} download attempts failed for '{query}'")
    return False