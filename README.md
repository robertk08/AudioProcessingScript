# Audio Processing Tool

A Python tool for batch downloading, trimming, and processing audio clips from YouTube videos using data from a CSV file. Ideal for projects, education, or events where you need consistent, automated audio processing.

---

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [CSV Format](#csv-format)
6. [Usage](#usage)
7. [Logging](#logging)
8. [Contributing & Support](#contributing--support)

---

## Features

- 🔍 Download audio from YouTube search results  
- ✂️ Trim clips at specified start times  
- ⚙️ Fully configurable clip settings (duration: 40s, format: MP3 @ 320k)  
- 🎚️ Audio processing: normalization to -20 dBFS, fade in & out  
- 🚀 Parallel processing for fast batch handling  
- 🖥️ Optional Streamlit-based UI for interactive control  
- 📊 Visual progress bars & live success status  
- 📝 Logging to `processes.log` with fresh logs per run

---

## Requirements

- Python 3.7 or higher
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [pydub](https://github.com/jiaaro/pydub)
- [tqdm](https://github.com/tqdm/tqdm)
- [streamlit](https://streamlit.io/) (optional, for UI)
- [ffmpeg](https://ffmpeg.org/) (must be in your system PATH)

All Python dependencies are listed in `requirements.txt`.

---

## Installation

1. **Install Python** (if not already installed).
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install ffmpeg:**
   - macOS: `brew install ffmpeg`
   - Windows: Download from https://ffmpeg.org/download.html and add `ffmpeg/bin` to your PATH.

> **Note:** `ffmpeg` must be available in your system `PATH` for the scripts to function correctly.

---

## Configuration

All settings are managed in `config.json`. Key sections include:

### General Settings
- `output_dir`: Directory for processed audio files
- `log_filename`: Log file name
- `filename_template`: Template for output filenames
- `cloud`: Enables cloud-related features (for UI; set to `false` for local use)
- `overwrite`: Overwrite existing files if true
- `parallel_workers`: Number of parallel processing jobs
- `default_clip_duration_seconds`: Default duration for each audio clip
- `max_download_retries`: Number of download retry attempts
- `retry_delay_seconds`: Delay between retries (seconds)

### Audio Settings (`audio_settings`)
- `format`: Output file format (e.g., `mp3`, `wav`)
- `bitrate`: Output bitrate (e.g., `320k`)
- `sample_rate`: Output sample rate (Hz)
- `target_dBFS`: Target loudness for normalization
- `normalize`: Whether to normalize audio
- `fade_in` / `fade_out`: Enable fade effects
- `fade_in_duration_ms` / `fade_out_duration_ms`: Fade durations (ms)

### CSV Settings (`csv_settings`)
- `file`: Path to the CSV file (default: `tests/shortertestdata.csv`)
- `delimiter`: CSV delimiter (default: `;`)
- `columns`: Mapping of internal field names to CSV column headers. Example:
  ```json
  "columns": {
    "name": "Name",
    "surname": "Surname",
    "song": "Song (Title & Artist)",
    "start_time": "Start Time (MM:SS)"
  }
  ```

*Edit `config.json` to match your CSV structure and desired output settings.*

---

## CSV Format

Your CSV file should have the following columns (headers can be customized in `config.json`):

| Column Header             | Description                                                                                 |
|--------------------------|---------------------------------------------------------------------------------------------|
| **Name**                 | The person's first name. Used for naming and identification.                                |
| **Surname**              | The person's last name. Used together with the first name for unique identification.        |
| **Song (Title & Artist)**| The full song title and artist name. Used to search for the correct audio track.            |
| **Start Time (MM:SS)**   | The time offset in the song where the clip should start. Format: minutes and seconds (e.g., 1:30). |

---

## Usage

### Command Line
1. Place your CSV file in the project folder (default: `tests/shortertestdata.csv`).
2. Edit `config.json` as needed (especially the `csv_settings.columns` mapping and output directory).
3. Run the script:
   ```bash
   python main.py
   ```
4. Processed audio files will appear in the configured output directory.

### Streamlit UI (Optional)
1. Ensure `streamlit` is installed.
2. Run the UI:
   ```bash
   streamlit run UI.py
   ```
3. Use the web interface to configure and launch processing jobs.
   > **Note:** Set `cloud` to `false` in `config.json` for local UI operation.

---

## Logging

- Logs are saved to the file specified in `log_filename` (default: `processes.log`).
- Each run creates a fresh log.
- Logs include timestamps, thread info, success markers, and errors.

---

## Contributing & Support

- Found a bug? [Open an issue](https://github.com/robertk08/AudioProcessingScript/issues)
- Want to improve the project? Submit a pull request!
- Questions? Contact the author or contribute via the repository.