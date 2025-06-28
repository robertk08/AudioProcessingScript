import logging
import zipfile
import shutil
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


def copy_log_file(config: Dict[str, Any], output_dir: Path) -> None:
    log_path: Path = Path(config.get("log_filename", "processes.log"))
    
    if not log_path.is_absolute():
        log_path = Path.cwd() / log_path
    
    if log_path.exists():
        try:
            dest_log_path: Path = output_dir / log_path.name
            if log_path.resolve() != dest_log_path.resolve():
                shutil.copy2(log_path, dest_log_path)
        except Exception as e:
            logging.warning(f"Failed to copy log file to output directory: {e}")


def zip_files(directory: Path, config: Dict[str, Any]) -> None:
    copy_log_file(config, directory)
    if not config.get("zip_output", False):
        return
        
    zip_path: Path = directory / f"{config.get('zip_name', 'audio_files')}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in directory.iterdir():
            if file.is_file() and file.suffix != ".zip":
                zipf.write(file, arcname=file.name)
    
    extensions: Set[str] = {file.suffix.lower() for file in directory.iterdir() 
                           if file.is_file() and file.suffix != ".zip"}
    cleanup_files(directory, extensions)