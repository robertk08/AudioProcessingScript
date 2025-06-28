import csv
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from pathlib import Path
from typing import Any, Dict, Optional
from .process_row import process_row
from .utils import zip_files, copy_log_file

def process_csv(
    csv_path: str,
    output_dir: Path,
    config: Dict[str, Any],
    csv_settings: Dict[str, Any],
    audio_settings: Dict[str, Any],
    progress: Optional[Any] = None
) -> None:
    delimiter: str = csv_settings.get("delimiter", ",")
    max_workers: int = config.get("parallel_workers", 4)
    
    try:
        with open(csv_path, newline='', encoding="utf-8") as f:
            rows = list(csv.DictReader(f, delimiter=delimiter))
        
        if not rows:
            logging.warning(f"CSV file is empty: {csv_path}")
            return
        
        total: int = len(rows)
        logging.info(f"CSV contains {total} rows: {csv_path}")
        failed: int = 0
        
        with tqdm(total=total, unit="file", dynamic_ncols=True) as bar, ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_row, row, output_dir, config, csv_settings, audio_settings): row for row in rows}
            
            for future in as_completed(futures):
                try:
                    if not future.result():
                        failed += 1
                except Exception as e:
                    failed += 1
                    logging.error(f"Error processing row {futures[future]}: {e}")
                finally:
                    bar.update(1)
                    if progress and callable(getattr(progress, "progress", None)):
                        try:
                            progress.progress(round(bar.n / total * 100))
                        except Exception as e:
                            logging.warning(f"Failed to update progress: {e}")
        
        logging.info(f"CSV processing complete. {failed} rows failed.")
        
        copy_log_file(config, output_dir)
        zip_files(output_dir, config)
        
    except FileNotFoundError:
        logging.error(f"CSV file not found: {csv_path}")
    except Exception as e:
        logging.error(f"Unexpected error while processing CSV: {e}")