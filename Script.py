import csv
import json
import subprocess
import time
import logging
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from pathlib import Path

# Load configuration from a JSON file
def load_config(path="config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()

# Convert timestamp string (MM:SS) to milliseconds
def timestamp_to_ms(ts):
    try:
        minutes, seconds = map(int, ts.strip().split(":"))
        return (minutes * 60 + seconds) * 1000
    except Exception as e:
        logging.error(f"Invalid start time '{ts}': {e}")
        return None

# Download a song from YouTube using yt-dlp with retries
def download_song(query, temp_path):
    max_retries = config.get("max_download_retries", 3)
    retry_delay = config.get("download_retry_delay", 5)
    audio_format = config.get("audio_format", "mp3")

    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", audio_format,
        "-o", temp_path.as_posix(),
        f"ytsearch1:{query}"
    ]

    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"Attempting download: '{query}', attempt {attempt}")
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError as e:
            logging.warning(f"Download attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(retry_delay)
    return False

# Trim and process the downloaded audio clip according to config settings
def trim_song(input_path, output_path, start_time):
    duration_sec = config.get("default_clip_duration_seconds", 30)
    normalize = config.get("normalize_audio", True)
    fade_in_enabled = config.get("fade_in", False)
    fade_in_duration = config.get("fade_in_duration_ms", 0)
    fade_out_enabled = config.get("fade_out", False)
    fade_out_duration = config.get("fade_out_duration_ms", 0)
    audio_format = config.get("audio_format", "mp3")
    bitrate = config.get("audio_bitrate", None)
    sample_rate = config.get("sample_rate", None)

    start_ms = timestamp_to_ms(start_time)
    if start_ms is None:
        logging.error(f"Invalid start time: {start_time}")
        return False

    try:
        audio = AudioSegment.from_file(input_path)
        end_ms = start_ms + duration_sec * 1000
        if end_ms > len(audio):
            end_ms = len(audio)
        snippet = audio[start_ms:end_ms]

        # Ensure output is stereo
        snippet = snippet.set_channels(2)

        # Normalize audio volume if enabled
        if normalize:
            snippet = match_target_amplitude(snippet)

        # Apply fade-in effect if configured
        if fade_in_enabled and fade_in_duration > 0:
            snippet = snippet.fade_in(fade_in_duration)

        # Apply fade-out effect if configured
        if fade_out_enabled and fade_out_duration > 0:
            snippet = snippet.fade_out(fade_out_duration)

        export_kwargs = {}
        if bitrate and audio_format.lower() == "mp3":
            export_kwargs["bitrate"] = bitrate
        if sample_rate:
            export_kwargs["parameters"] = ["-ar", str(sample_rate)]

        snippet.export(output_path, format=audio_format, **export_kwargs)
        return True
    except Exception as e:
        logging.error(f"Error while trimming: {e}")
        return False

# Normalize audio to target dBFS level
def match_target_amplitude(sound):
    target_dBFS = config.get("target_dBFS", -20.0)
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

# Process a single CSV row: download, trim, and save the audio clip
def process_row(row, output_dir):
    csv_columns = config["csv_columns"]
    audio_format = config.get("audio_format", "mp3")
    overwrite_existing_files = config.get("overwrite_existing_files", False)

    first_name = row.get(csv_columns["name"], "").strip()
    last_name = row.get(csv_columns["surname"], "").strip()
    song = row.get(csv_columns["song"], "").strip()
    start_time = row.get(csv_columns["start_time"], "").strip()

    # Skip rows with missing essential data
    if not first_name or not last_name or not song or not start_time:
        logging.info(f"Skipping incomplete row: {row}")
        return

    filename_base = f"{last_name}, {first_name}"
    final_path = output_dir / f"{filename_base}.{audio_format}"
    temp_path = output_dir / f"{filename_base}_full.%(ext)s"

    # Skip processing if output file exists and overwrite is disabled
    if final_path.exists() and not overwrite_existing_files:
        logging.info(f"File already exists and overwrite is False: {final_path}")
        return

    logging.info(f"Starting processing: {first_name} {last_name}, Song: {song}, Start time: {start_time}")

    # Download the full song audio
    if not download_song(song, temp_path):
        logging.error(f"Download failed for {song}")
        return

    downloaded_file = temp_path.with_name(temp_path.name.replace("%(ext)s", audio_format))

    # Trim and save the audio clip
    if not trim_song(downloaded_file, final_path, start_time):
        logging.error(f"Trimming failed for {final_path}")
        return

    # Clean up the downloaded full audio file
    if downloaded_file.exists():
        downloaded_file.unlink()

    logging.info(f"Successfully saved: {final_path}")

# Process the entire CSV file in parallel using threads
def process_csv(csv_path, output_dir):
    # Retrieve CSV delimiter and parallelism settings from config
    delimiter = config.get("csv_delimiter", ",")
    max_workers = config.get("parallel_workers", 4)

    with open(csv_path, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        rows = list(reader)

    progress_bar = tqdm(
        total=len(rows),
        unit="file",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
        dynamic_ncols=True,
        leave=True
    )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_row = {executor.submit(process_row, row, output_dir): row for row in rows}
        for future in as_completed(future_to_row):
            row = future_to_row[future]
            first_name = row.get(config["csv_columns"]["name"], "").strip()
            last_name = row.get(config["csv_columns"]["surname"], "").strip()
            filename_base = f"{last_name}, {first_name}" if last_name or first_name else "Unknown"
            tqdm.write(f"Processing: {filename_base}")
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error during parallel processing for row {row}: {e}")
            progress_bar.update(1)
    progress_bar.close()

# Setup logging configuration to file
def setup_logging():
    log_file = config.get("log_file", "process.log")
    # Clear existing log file content
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

if __name__ == "__main__":
    output_dir = Path(config.get("output_dir", "./output")).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    setup_logging()

    csv_file = config.get("csv_file", "testdata.csv")
    process_csv(csv_file, output_dir)