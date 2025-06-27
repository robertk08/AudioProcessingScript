import logging
import re
from pathlib import Path

from .audio_processor import trim_song
from .downloader import download_song

def build_filename(row_data, config):
    template = config.get("filename_template", "{surname}, {name}")
    try:
        filename = template.format(
            name=row_data.get("name", ""),
            surname=row_data.get("surname", ""),
            song=row_data.get("song", ""),
            start_time=row_data.get("start_time", "")
        )
    except Exception as e:
        logging.error(f"Filename formatting error: {e} with data: {row_data}")
        raise
    filename = re.sub(r'\s+', ' ', filename).strip()
    
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return filename

def process_row(row, output_dir, config, csv_settings, audio_settings):
    csv_columns = csv_settings.get("columns", {})
    audio_format = audio_settings.get("format", "mp3")
    overwrite_existing_files = config.get("overwrite", False)

    for key in ["name", "surname", "song", "start_time"]:
        column_header = csv_columns.get(key, "")
        if column_header not in row:
            logging.error(f"Missing CSV column '{column_header}' for key '{key}' in row: {row}")
            return None

    name = row.get(csv_columns.get("name", ""), "").strip()
    surname = row.get(csv_columns.get("surname", ""), "").strip()
    song = row.get(csv_columns.get("song", ""), "").strip()
    start_time = row.get(csv_columns.get("start_time", ""), "").strip()

    if not name or not surname or not song or not start_time:
        logging.info(f"Skipping incomplete row: {row}")
        return None

    row_data = {
        "name": name,
        "surname": surname,
        "song": song,
        "start_time": start_time
    }

    try:
        filename_base = build_filename(row_data, config)
    except Exception:
        return None

    logging.debug(f"Built filename base: {filename_base}")

    final_path = output_dir / f"{filename_base}.{audio_format}"
    temp_path_template = output_dir / f"{filename_base}.%(ext)s"
    logging.debug(f"Final path: {final_path}")
    logging.debug(f"Temporary path template: {temp_path_template}")

    if final_path.exists() and not overwrite_existing_files:
        logging.info(f"File already exists: {final_path}")
        return None

    logging.info(f"Processing: {name} {surname}, Song: {song}, Start: {start_time}")

    if not download_song(song, temp_path_template, config, audio_settings):
        logging.error(f"Download failed: {song}")
        return None

    downloaded_file = Path(str(temp_path_template).replace("%(ext)s", audio_format))

    if not trim_song(downloaded_file, final_path, start_time, config, audio_settings):
        logging.error(f"Trim failed: {final_path}")
        return None

    logging.info(f"Saved: {final_path}")