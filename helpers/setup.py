from pathlib import Path
import logging
import json
import tempfile

from .utils import cleanup_files


def load_config(path="config.json"):
    try:
        path = Path(path).expanduser().resolve()
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file '{path}' not found.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")


def setup_logging(config):
    log_file = config.get("log_filename", "processes.log")
    Path(log_file).write_text("", encoding="utf-8")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def prepare_output_directory(config):
    is_cloud = config.get("cloud", False)
    output_dir = (
        Path(tempfile.gettempdir()) / "audioprocessing_output"
        if is_cloud
        else Path(config.get("output_dir", "./output")).expanduser()
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    if is_cloud or config.get("overwrite", False):
        cleanup_files(output_dir, {".webm", ".mp3", ".wav", ".zip"})
    return output_dir


def initialize():
    config = load_config()
    setup_logging(config)
    csv_settings = config.get("csv_settings", {})
    audio_settings = config.get("audio_settings", {})
    csv_file = csv_settings.get("file", "testdata.csv")
    output_dir = prepare_output_directory(config)
    return csv_file, output_dir, config, csv_settings, audio_settings