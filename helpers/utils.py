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
    zip_path: Path = directory / f"{config.get('zip_name', 'audio_files')}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in directory.iterdir():
            if file.is_file() and file.suffix != ".zip":
                zipf.write(file, arcname=file.name)
        
        log_path: Path = directory / config.get('log_filename', 'processes.log')
        if log_path.exists():
            zipf.write(log_path, arcname=log_path.name)
    extensions: Set[str] = {file.suffix.lower() for file in directory.iterdir() if file.is_file() and file.suffix != ".zip"}
    cleanup_files(directory, extensions)