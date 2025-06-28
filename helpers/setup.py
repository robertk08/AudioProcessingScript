from pathlib import Path
import logging
import json
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
    log_path: Path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def prepare_output_directory(config: Dict[str, Any]) -> Path:
    output_dir: Path = Path(config.get("output_dir", "./output")).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    if config.get("overwrite", False):
        cleanup_files(output_dir, {".webm", ".mp3", ".wav", ".zip", ".log"})
    return output_dir


def initialize() -> Tuple[str, Path, Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    config: Dict[str, Any] = load_config()
    setup_logging(config)
    csv_settings: Dict[str, Any] = config.get("csv_settings", {})
    audio_settings: Dict[str, Any] = config.get("audio_settings", {})
    csv_file: str = csv_settings.get("file", "testdata.csv")
    output_dir: Path = prepare_output_directory(config)
    return csv_file, output_dir, config, csv_settings, audio_settings