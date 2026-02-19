import subprocess
import logging
import time
import sys
from pathlib import Path
from typing import Dict, Any

def download_song(
    query: str,
    temp_path: Path,
    config: Dict[str, Any],
    audio_settings: Dict[str, Any],
    is_link: bool = False
) -> bool:
    max_retries: int = config.get("max_download_retries", 3); retry_delay: int = config.get("retry_delay_seconds", 5)
    audio_format: str = audio_settings.get("format", "mp3").lower(); yt_dlp_extractor_args: str = config.get("yt_dlp_extractor_args", "youtube:player_client=android,web")
    
    command: list[str] = [
        sys.executable, "-m", "yt_dlp", "--extract-audio",
        "--no-playlist", "--no-progress",
        "--extractor-args", yt_dlp_extractor_args,
        "--audio-format", audio_format, "--audio-quality", "0",
        "-f", "bestaudio/best",
        "-o", temp_path.as_posix(),
        query if is_link else f"ytsearch1:{query}"
    ]
    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"Attempting download: '{query}', attempt {attempt}")
            subprocess.run(command, check=True, capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            yt_dlp_output: str = ((e.stderr or e.stdout) or "").strip().replace("\n", " | ")[:600]
            logging.warning(f"Download attempt {attempt} failed for '{query}' (exit code {e.returncode}): {yt_dlp_output or 'No yt-dlp output'}")
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                logging.error(f"All {max_retries} download attempts failed for '{query}'")
    return False
