from helpers.setup import initialize
from helpers.process_csv import process_csv
import logging

if __name__ == "__main__":
    try:
        csv_file, output_dir, config, csv_settings, audio_settings = initialize()
        process_csv(csv_file, output_dir, config, csv_settings, audio_settings)
    except Exception as e:
        logging.exception("Fatal error occurred during audio processing:")
        exit(1)