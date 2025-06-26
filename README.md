# Audio Processing Script

A Python script that automates downloading, trimming, and exporting audio clips from YouTube based on a CSV playlist.

## Table of Contents

1. [Features](#features)  
2. [Requirements](#requirements)  
3. [Installation](#installation)  
4. [Configuration](#configuration)  
5. [CSV Format](#csv-format)  
6. [Usage](#usage)  
7. [Logging](#logging)  
8. [Support & Contribution](#support--contribution)

---

## Features

- 🔍 Download audio from YouTube search results  
- ✂️ Trim clips at specified start times  
- ⚙️ Fully configurable clip settings (duration: 40s, format: MP3 @ 320k)  
- 🎚️ Audio processing: normalization to -20 dBFS, fade in (5s) & out (15s)  
- 🚀 Parallel processing (up to 15 threads) for fast batch handling  
- 📄 Flexible CSV mapping: `Name`, `Nachname`, `Lied (Titel & Künstler)`, `Startzeit (Minute/Sekunde)`  
- 🖥️ Streamlit-based UI for interactive control  
- 📊 Visual progress bars & live success status  
- 📝 Logging to `processes.log` with fresh logs per run

## Requirements

- Python 3.7 or higher  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)  
- [pydub](https://github.com/jiaaro/pydub)  
- [tqdm](https://github.com/tqdm/tqdm)  
- [streamlit](https://streamlit.io/)  
- [ffmpeg](https://ffmpeg.org/) must be available in your system PATH  

All Python dependencies are listed in `requirements.txt`.

## Installation

1. **Install Python** if not already installed.  
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Install ffmpeg**:
   - macOS (Homebrew): `brew install ffmpeg`  
   - Windows: Download from https://ffmpeg.org/download.html and add `ffmpeg/bin` to your PATH.  

*Note:* `ffmpeg` must be available in your system `PATH` for the scripts to function.

## Configuration

All settings are stored in `config.json`. Key sections include:

### General
- `output_dir` (string): Directory where the processed clips will be saved.  
- `log_filename` (string): Name of the file where logs will be written.  
- `overwrite` (bool): If true, existing audio files will be overwritten.  
- `parallel_workers` (int): Number of audio downloads/processing tasks to run in parallel.  
- `default_clip_duration_seconds` (int): Default length of each trimmed audio clip.  
- `max_download_retries` (int): Number of retry attempts for failed downloads.  
- `retry_delay_seconds` (int): Delay (in seconds) between download retries.  

### Audio Settings (`audio_settings`)
- `format` (string): Output file format, such as `mp3` or `wav`.  
- `bitrate` (string): Desired bitrate for the audio output.  
- `sample_rate` (int): Target sample rate for the audio in Hz.  
- `target_dBFS` (float): Target loudness level for normalization in decibels.  
- `fade_in` / `fade_out` (bool): Whether to apply fade effects at the beginning/end.  
- `fade_in_duration_ms` / `fade_out_duration_ms` (int): Duration of fade effects in milliseconds.  
- `normalize` (bool): Whether to normalize the volume of the audio.

### CSV Settings (`csv_settings`)
- `file` (string): Name of the CSV file to use for batch processing.  
- `delimiter` (string): Character used to separate columns in the CSV.  
- `columns` (object): Mapping of expected column keys to the headers used in your CSV:
  - `name`: Column in the csv file that describes the person’s first name  
  - `surname`: Column in the csv file that describes the person’s last name  
  - `song`: column in the csv file that describes the song entry (title & artist)  
  - `start_time`: column in the csv file that describes the where in the song to begin clipping (in MM:SS format)

*Tip:* Adjust these values in the `config.json` file to suit your needs.

## CSV Format

Your CSV should include headers matching the values in `csv_settings.columns`, for example:

```csv
Name;Nachname;Lied (Titel & Künstler);Startzeit (Minute/Sekunde)
Lena;Miller;Imagine Dragons - Believer;00:23
```

- **Delimiter** must match `csv_settings.delimiter`.  
- **Start times** in `MM:SS` format.

## Usage

1. Place your CSV file in the project directory.  
2. Edit `config.json` to set your preferences.  
3. Run the script:
   ```bash
   python Script.py
   ```
4. (Optional) Launch the Streamlit interface:
   ```bash
   streamlit run UI.py
   ```
5. Use the web interface to select your CSV and configure the run interactively.
6. Check the output directory for processed clips.  

## Logging

- Progress and errors are logged to the file specified in `log_filename` (default: `process.log`).  
- Each run clears the previous log, so you start with a fresh log on every execution.
- Logs now include detailed timestamps and success markers for easier debugging and tracking.

## Support & Contribution

Feel free to open issues or submit pull requests on the project repository. For questions, contact the author.