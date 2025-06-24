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

- Download audio from YouTube search results  
- Trim clips at specified start times  
- Configurable clip duration, fade in/out, normalization, sample rate, bitrate, and more  
- Parallel processing for faster batch operations  
- Flexible CSV column mapping and delimiter settings  
- Streamlit-based user interface for interactive use
- Visual progress bar and success status
- Automatic logging and live feedback during batch processing

## Requirements

- Python 3.7 or higher  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)  
- [pydub](https://github.com/jiaaro/pydub)  
- [tqdm](https://github.com/tqdm/tqdm)  
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)  
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

All settings are stored in `config.json`. Key options include:

- `output_dir` (string): Directory to save processed clips.  
- `csv_file` (string): CSV filename in project root.  
- `csv_delimiter` (string): Character to separate columns (e.g., `;` or `,`).  
- `csv_columns` (object): Map logical fields to your CSV headers:
  - `name`: First name column header  
  - `surname`: Last name column header  
  - `song`: Song title & artist column header  
  - `start_time`: Clip start time column header  
- `default_clip_duration_seconds` (int): Length of each clip in seconds.  
- `audio_format` (string): Output format (`mp3`, `wav`).  
- `audio_bitrate` (string): Bitrate for MP3 *only for mp3* (e.g., `192k`).  
- `sample_rate` (int): Output sample rate in Hz *only for wav* (e.g., `44100`).  
- `fade_in` / `fade_out` (bool): Apply fade effects.  
- `fade_in_duration_ms` / `fade_out_duration_ms` (int): Fade durations in milliseconds.  
- `normalize_audio` (bool): Enable volume normalization.  
- `target_dBFS` (float): Target normalization level in dBFS (e.g., `-20.0`).  
- `max_download_retries` (int): Number of download attempts.  
- `retry_delay_seconds` (int): Delay between retries.  
- `overwrite_existing_files` (bool): Overwrite existing outputs or skip.  
- `parallel_workers` (int, optional): Number of concurrent threads (if set).

*Tip:* Adjust these values to fine-tune performance and output quality.

## CSV Format

Your CSV should include headers matching the values in `csv_columns`, for example:

```csv
First Name;Last Name;Song (Title & Artist);Start Time (Minute/Second)
Lena ;Miller;Imagine Dragons - Believer;00:23
```

- **Delimiter** must match `csv_delimiter`.  
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

- Progress and errors are logged to the file specified in `log_file` (default: `process.log`).  
- Each run clears the previous log, so you start with a fresh log on every execution.
- Logs now include detailed timestamps and success markers for easier debugging and tracking.

## Support & Contribution

Feel free to open issues or submit pull requests on the project repository. For questions, contact the author.