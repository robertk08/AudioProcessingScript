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
8. [Testing & Code Quality](#testing--code-quality)
9. [Contributing & Support](#contributing--support)

---

## Features

- 🔍 Download audio from YouTube search results or direct links  
- 🔗 Support for direct YouTube URLs (when provided in CSV) with fallback to song name search
- ✂️ Trim clips at specified start times  
- ⚙️ Fully configurable clip settings (duration, format, bitrate, sample rate, normalization, fade in/out)  
- 🎚️ Audio processing: normalization to target dBFS, fade in & out  
- 🚀 Parallel processing for fast batch handling  
- 🖥️ Optional Streamlit-based UI for interactive control  
- 📊 Visual progress bars & live success status  
- 📝 Logging to `processes.log` with fresh logs per run  
- 🛡️ Robust error handling and configuration validation

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
- `zip_output`: If true, output files are zipped after processing
- `zip_name`: Name of the output zip file
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
    "start_time": "Start Time (MM:SS)",
    "link": "Link"
  }
  ```

*Edit `config.json` to match your CSV structure and desired output settings.*

---

## CSV Format

Your CSV file should have the following columns (headers can be customized in `config.json`):

| Column Header                  | Description                                                                                 |
|------------------------------- |--------------------------------------------------------------------------------------------|
| **Name**                       | The person's first name. Used for naming and identification.                               |
| **Surname**                    | The person's last name. Used together with the first name for unique identification.       |
| **Song (Title & Artist)**      | The full song title and artist name. Used to search for the correct audio track when no link is provided. |
| **Start Time (MM:SS)**         | The time offset in the song where the clip should start. Format: minutes and seconds (e.g., 01:30). |
| **Link**                       | *(Optional)* Direct YouTube URL. If provided, this link will be used for downloading instead of searching by song name. |

**Note:** The Link column is optional. If a link is provided, it will be used directly for downloading. If no link is provided or the link field is empty, the system will fall back to searching YouTube using the song name and artist.

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

---

## Logging

- Logs are saved to the file specified in `log_filename` (default: `processes.log`).
- Each run creates a fresh log.
- Logs include timestamps, thread info, success markers, and errors.

---

## Testing & Code Quality

- All core modules use **type hints** for better readability and maintainability.
- The codebase is structured for easy testing and extension.

---

## Contributing & Support

- Found a bug? [Open an issue](https://github.com/robertk08/AudioProcessingScript/issues)
- Want to improve the project? Submit a pull request!
- Questions? Contact the author or contribute via the repository.

---

**Tip:**  
For best results, keep your dependencies up to date and review the logs for any failed downloads or processing errors.  
If you encounter issues with ffmpeg or yt-dlp, check your system PATH and ensure all dependencies are installed.