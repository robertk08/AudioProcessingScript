from helpers.setup import initialize
from helpers.process_csv import process_csv

if __name__ == "__main__":
    config, csv_settings, audio_settings, output_dir, csv_file = initialize()
    process_csv(csv_file, output_dir, config, csv_settings, audio_settings)