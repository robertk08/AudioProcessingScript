import csv
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from pathlib import Path
from typing import Any, Dict, Optional, Callable
from .process_row import process_row
from .utils import zip_files

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
        bar = tqdm(total=total, unit="file", dynamic_ncols=True)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_row, row, output_dir, config, csv_settings, audio_settings): row for row in rows}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result is None or result is False:
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
        bar.close()
        logging.info(f"CSV processing complete. {failed} rows failed.")
        
        log_filename = config.get("log_filename", "processes.log")
        log_path = Path(log_filename)
        if not log_path.is_absolute():
            log_path = Path.cwd() / log_path
        if log_path.exists():
            try:
                dest_log_path = output_dir / log_path.name
                if log_path.resolve() != dest_log_path.resolve():
                    with open(log_path, "rb") as src, open(dest_log_path, "wb") as dst:
                        dst.write(src.read())
            except Exception as e:
                logging.warning(f"Failed to copy log file to output directory: {e}")
            
        if config.get("zip_output", False):
            zip_files(output_dir, config)
    except FileNotFoundError:
        logging.error(f"CSV file not found: {csv_path}")
    except Exception as e:
        logging.error(f"Unexpected error while processing CSV: {e}")