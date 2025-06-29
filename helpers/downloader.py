import subprocess
import logging
import time
from pathlib import Path
from typing import Dict, Any

def download_song(
    query: str,
    temp_path: Path,
    config: Dict[str, Any],
    audio_settings: Dict[str, Any],
    is_link: bool = False
) -> bool:
    max_retries: int = config.get("max_download_retries", 3)
    retry_delay: int = config.get("retry_delay_seconds", 5)
    audio_format: str = audio_settings.get("format", "mp3").lower()
    
    download_url: str = query if is_link else f"ytsearch1:{query}"
    
    command: list[str] = [
        "yt-dlp", "--extract-audio",
        "--audio-format", audio_format,
        "--audio-quality", "0",
        "-f", "bestaudio/best",
        "-o", temp_path.as_posix(),
        download_url
    ]
    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"Attempting download: '{query}', attempt {attempt}")
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, text=True)
            return True
        except subprocess.CalledProcessError as e:
            logging.warning(f"Download attempt {attempt} failed for '{query}': {e}")
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                logging.error(f"All {max_retries} download attempts failed for '{query}'")
    return False