from pathlib import Path
import logging
import json
import tempfile
from typing import Dict, Any, Tuple
from .utils import cleanup_files


def load_config(path: str = "config.json") -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file '{path}' not found.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")


def setup_logging(config: Dict[str, Any]) -> None:
    log_file: str = config.get("log_filename", "processes.log")
    Path(log_file).write_text("")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def prepare_output_directory(config: Dict[str, Any]) -> Path:
    if config.get("cloud", False):
        temp_dir_path: Path = Path(tempfile.gettempdir()) / "audioprocessing_output"
        temp_dir_path.mkdir(parents=True, exist_ok=True)
        if config.get("cloud", False) or config.get("overwrite", False):
            cleanup_files(temp_dir_path, {".webm", ".mp3", ".wav", ".zip"})
        return temp_dir_path
    else:
        output_dir_path: Path = Path(config.get("output_dir", "./output")).expanduser()
        output_dir_path.mkdir(parents=True, exist_ok=True)
        if config.get("cloud", False) or config.get("overwrite", False):
            cleanup_files(output_dir_path, {".webm", ".mp3", ".wav", ".zip"})
        return output_dir_path


def initialize() -> Tuple[str, Path, Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    config: Dict[str, Any] = load_config()
    setup_logging(config)
    csv_settings: Dict[str, Any] = config.get("csv_settings", {})
    audio_settings: Dict[str, Any] = config.get("audio_settings", {})
    csv_file: str = csv_settings.get("file", "testdata.csv")
    output_dir: Path = prepare_output_directory(config)
    return csv_file, output_dir, config, csv_settings, audio_settings