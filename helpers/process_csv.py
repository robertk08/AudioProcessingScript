# csv_runner.py
import csv
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from pathlib import Path
from .process_row import process_row

def process_csv(csv_path, output_dir, config, csv_settings, audio_settings, progress=None):
    delimiter = csv_settings.get("delimiter", ",")
    max_workers = config.get("parallel_workers", 4)

    with open(csv_path, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        rows = list(reader)

    total_rows = len(rows)
    progress_bar = None
    if not progress:
        progress_bar = tqdm(total=total_rows, unit="file", dynamic_ncols=True)

    completed = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_row, row, output_dir, config, csv_settings, audio_settings): row
            for row in rows
        }
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Parallel error: {e}")
            completed += 1
            if progress:
                progress.progress(int(completed / total_rows * 100))
            elif progress_bar:
                progress_bar.update(1)

    if progress_bar:
        progress_bar.close()