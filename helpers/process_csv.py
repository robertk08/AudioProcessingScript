import csv
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from .process_row import process_row
from .utils import zip_files


def process_csv(csv_path, output_dir, config, csv_settings, audio_settings, progress=None):
    delimiter = csv_settings.get("delimiter", ",")
    max_workers = config.get("parallel_workers", 4)

    try:
        with open(csv_path, newline='', encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=delimiter)
            rows = list(reader)

        total_rows = len(rows)
        logging.info(f"CSV contains {total_rows} rows: {csv_path}")

        failed_count = 0
        progress_bar = tqdm(total=total_rows, unit="file", dynamic_ncols=True)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_row = {
                executor.submit(process_row, row, output_dir, config, csv_settings, audio_settings): row
                for row in rows
            }

            for future in as_completed(future_to_row):
                try:
                    future.result()
                except Exception as e:
                    failed_count += 1
                    logging.error(f"Error processing row {future_to_row[future]}: {e}")
                finally:
                    progress_bar.update(1)
                    if progress and callable(getattr(progress, "progress", None)):
                        try:
                            progress.progress(round(progress_bar.n / total_rows * 100))
                        except Exception as e:
                            logging.warning(f"Failed to update progress: {e}")

        progress_bar.close()
        logging.info(f"CSV processing complete. {failed_count} rows failed.")

        if config.get("zip_output", False):
            zip_files(output_dir, config)

    except FileNotFoundError:
        logging.error(f"CSV file not found: {csv_path}")
    except Exception as e:
        logging.error(f"Unexpected error while processing CSV: {e}")