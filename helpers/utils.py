import logging
import zipfile
from pathlib import Path


def timestamp_to_ms(ts):
    try:
        parts = ts.strip().split(":")
        if len(parts) != 2:
            raise ValueError("Expected format MM:SS")
        minutes, seconds = map(int, parts)
        return (minutes * 60 + seconds) * 1000
    except (ValueError, IndexError) as e:
        logging.error(f"Invalid start time '{ts}': {e}")
        return None


def cleanup_files(output_dir: Path, extensions: set):
    logging.info(f"Cleaning up files in {output_dir} with extensions: {extensions}")
    for file in output_dir.iterdir():
        if file.suffix.lower() in extensions and file.is_file():
            try:
                file.unlink()
            except Exception as e:
                logging.warning(f"Failed to delete {file.name}: {e}")


def zip_files(output_dir: Path, config):
    zip_name = config.get("zip_name", "audio_files") + ".zip"
    zip_path = output_dir / zip_name

    logging.info(f"Creating ZIP archive at: {zip_path}")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in output_dir.iterdir():
            if file.is_file() and file.suffix != ".zip":
                zipf.write(file, arcname=file.name)

    logging.info("ZIP created. Cleaning up...")

    extensions_to_delete = {
        file.suffix.lower()
        for file in output_dir.iterdir()
        if file.is_file() and file.suffix != ".zip"
    }

    cleanup_files(output_dir, extensions_to_delete)