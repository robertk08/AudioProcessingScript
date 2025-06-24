import logging
from pathlib import Path
from .downloader import download_song
from .audio_processor import trim_song

def process_row(row, output_dir, config, csv_settings, audio_settings):
    csv_columns = csv_settings.get("columns", {})
    audio_format = audio_settings.get("format", "mp3")
    overwrite_existing_files = config.get("overwrite", False)

    first_name = row.get(csv_columns.get("name", ""), "").strip()
    last_name = row.get(csv_columns.get("surname", ""), "").strip()
    song = row.get(csv_columns.get("song", ""), "").strip()
    start_time = row.get(csv_columns.get("start_time", ""), "").strip()

    if not first_name or not last_name or not song or not start_time:
        logging.info(f"Skipping incomplete row: {row}")
        return

    filename_base = f"{last_name}, {first_name}"
    final_path = output_dir / f"{filename_base}.{audio_format}"
    temp_path = output_dir / f"{filename_base}_full.%(ext)s"

    if final_path.exists() and not overwrite_existing_files:
        logging.info(f"File already exists: {final_path}")
        return

    logging.info(f"Processing: {first_name} {last_name}, Song: {song}, Start: {start_time}")

    if not download_song(song, temp_path, config, audio_settings):
        logging.error(f"Download failed: {song}")
        return

    downloaded_file = temp_path.with_name(temp_path.name.replace("%(ext)s", audio_format))

    if not trim_song(downloaded_file, final_path, start_time, config, audio_settings):
        logging.error(f"Trim failed: {final_path}")
        return

    if downloaded_file.exists():
        downloaded_file.unlink()

    logging.info(f"Saved: {final_path}")
