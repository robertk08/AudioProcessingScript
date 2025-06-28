import logging
import re
from pathlib import Path
from typing import Optional, Dict, Any

from .audio_processor import trim_song
from .downloader import download_song

def process_row(
    row: Dict[str, Any], 
    output_dir: Path, 
    config: Dict[str, Any], 
    csv_settings: Dict[str, Any], 
    audio_settings: Dict[str, Any]
) -> Optional[bool]:
    columns: Dict[str, Any] = csv_settings.get("columns", {})
    audio_format: str = audio_settings.get("format", "mp3")
    overwrite: bool = config.get("overwrite", False)

    for key in ["surname", "name", "song", "start_time"]:
        col: str = columns.get(key, "")
        if col not in row:
            logging.error(f"Missing CSV column '{col}' for key '{key}' in row: {row}")
            return None
        
    surname: str = row.get(columns["surname"], "").strip()
    name: str = row.get(columns["name"], "").strip()
    song: str = row.get(columns["song"], "").strip()
    start_time: str = row.get(columns["start_time"], "").strip() or "0:00"

    if not all([surname, name, song, start_time]):
        logging.info(f"Skipping incomplete row: {row}")
        return None

    row_data: Dict[str, Any] = {"surname": surname, "name": name, "song": song, "start_time": start_time}
    template: str = config.get("filename_template", "{surname}, {name}")
    
    try:
        filename: str = template.format(**row_data)
    except Exception as e:
        logging.error(f"Filename formatting error: {e} with data: {row}")
        return None
    
    filename = re.sub(r'\s+', ' ', filename).strip()
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)

    final_path: Path = output_dir / f"{filename}.{audio_format}"
    temp_path: Path = output_dir / f"{filename}.%(ext)s"

    if final_path.exists() and not overwrite:
        logging.info(f"File already exists: {final_path}")
        return None

    logging.info(f"Processing: {name} {surname}, Song: {song}, Start: {start_time}")

    try:
        if not download_song(song, temp_path, config, audio_settings):
            logging.error(f"Download failed: {song}")
            return False

        downloaded_file: Path = Path(str(temp_path).replace("%(ext)s", audio_format))
        if not downloaded_file.exists() or downloaded_file.stat().st_size == 0:
            logging.error(f"Downloaded file is invalid: {downloaded_file}")
            return False

        if not trim_song(str(downloaded_file), str(final_path), start_time, config, audio_settings):
            logging.error(f"Trim failed: {final_path}")
            return False

        logging.info(f"Saved: {final_path}")
        return True
    except Exception as e:
        logging.error(f"Unexpected error in process_row: {e}")
        return False