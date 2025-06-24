from pathlib import Path
import logging
import json

def load_config(path="config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def setup_logging(config):
    log_file = config.get("log_filename", "processes.log")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("")  # Clear existing logs
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def initialize():
    config = load_config()
    csv_settings = config.get("csv_settings", {})
    audio_settings = config.get("audio_settings", {})
    output_dir = Path(config.get("output_dir", "./output")).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    setup_logging(config)
    return config, csv_settings, audio_settings, output_dir