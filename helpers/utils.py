import logging
import zipfile
from pathlib import Path
from typing import Optional, Set, Dict, Any


def timestamp_to_ms(timestamp: str) -> Optional[int]:
    try:
        minutes, seconds = map(int, timestamp.strip().split(":"))
        if minutes < 0 or seconds < 0 or seconds >= 60:
            raise ValueError
        return (minutes * 60 + seconds) * 1000
    except Exception:
        logging.error(f"Invalid start time '{timestamp}'")
        return None


def cleanup_files(directory: Path, extensions: Set[str]) -> None:
    for file in directory.iterdir():
        if file.is_file() and file.suffix.lower() in extensions:
            try:
                file.unlink()
            except Exception as e:
                logging.warning(f"Failed to delete {file.name}: {e}")


def zip_files(directory: Path, config: Dict[str, Any]) -> None:
    zip_name: str = f"{config.get('zip_name', 'audio_files')}.zip"
    zip_path: Path = directory / zip_name
    log_filename = config.get('log_filename', 'processes.log')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in directory.iterdir():
            if file.is_file() and file.suffix != ".zip":
                zipf.write(file, arcname=file.name)
        # Add log file if it exists and isn't already zipped
        log_path = directory / log_filename
        if log_path.exists() and log_path != zip_path:
            zipf.write(log_path, arcname=log_path.name)
    extensions: Set[str] = {file.suffix.lower() for file in directory.iterdir() if file.is_file() and file.suffix != ".zip"}
    cleanup_files(directory, extensions)