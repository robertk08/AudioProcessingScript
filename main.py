from pathlib import Path
from helpers.setup import initialize
from helpers.process_csv import process_csv

if __name__ == "__main__":
    config, csv_settings, audio_settings, output_dir = initialize()
    csv_file = csv_settings.get("file", "testdata.csv")
    process_csv(csv_file, output_dir, config, csv_settings, audio_settings)