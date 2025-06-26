from pathlib import Path
import logging
import json
import tempfile

def load_config(path="config.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file '{path}' not found.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")
    
def setup_logging(config):
    log_file = config.get("log_filename", "processes.log")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def prepare_output_directory(config):
    if config.get("cloud", False):
        output_dir = Path(tempfile.gettempdir()) / "audioprocessing_output"
    else:
        output_dir = Path(config.get("output_dir", "./output")).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    if config.get("cloud", False) and config.get("overwrite", True):
        for file in output_dir.iterdir():
            if file.suffix in (".webm", ".mp3", ".wav", ".part") and file.is_file():
                try:
                    file.unlink()
                except Exception as e:
                    logging.warning(f"Failed to delete {file.name}: {e}")

    return output_dir

def initialize():
    config = load_config()
    setup_logging(config)
    csv_settings = config.get("csv_settings", {})
    audio_settings = config.get("audio_settings", {})
    csv_file = csv_settings.get("file", "testdata.csv")

    output_dir = prepare_output_directory(config)

    return config, csv_settings, audio_settings, output_dir, csv_file