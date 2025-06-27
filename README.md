# Audio Processing Script

This script lets you batch download and trim audio from YouTube videos using CSV data — perfect for projects, schools, or events.

## Table of Contents

1. [✨ Features](#-features)  
2. [📦 Requirements](#-requirements)  
3. [⚙️ Installation](#-installation)  
4. [🛠️ Configuration](#-configuration)  
5. [📑 CSV Format](#-csv-format)  
6. [🚀 Usage](#-usage)  
7. [📋 Logging](#-logging)  
8. [🤝 Support & Contribution](#-support--contribution)

---

## ✨ Features

- 🔍 Download audio from YouTube search results  
- ✂️ Trim clips at specified start times  
- ⚙️ Fully configurable clip settings (duration: 40s, format: MP3 @ 320k)  
- 🎚️ Audio processing: normalization to -20 dBFS, fade in & out  
- 🚀 Parallel processing for fast batch handling  
- 🖥️ Streamlit-based UI for interactive control  
- 📊 Visual progress bars & live success status  
- 📝 Logging to `processes.log` with fresh logs per run

---

## 📦 Requirements

- Python 3.7 or higher  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)  
- [pydub](https://github.com/jiaaro/pydub)  
- [tqdm](https://github.com/tqdm/tqdm)  
- [streamlit](https://streamlit.io/)  
- [ffmpeg](https://ffmpeg.org/) must be available in your system PATH  

All Python dependencies are listed in `requirements.txt`.

---

## ⚙️ Installation

1. **Install Python** if not already installed.  

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install ffmpeg**:

   - macOS (Homebrew): `brew install ffmpeg`  
   - Windows: Download from https://ffmpeg.org/download.html and add `ffmpeg/bin` to your PATH.  

> **Note:**  
> `ffmpeg` must be available in your system `PATH` for the scripts to function correctly.

---

## 🛠️ Configuration

All settings are stored in `config.json`. Key sections include:

## General

- `output_dir` (string): Directory where the processed clips will be saved.  
- `log_filename` (string): Name of the file where logs will be written.  
- `filename_template` (string): Template for output filenames.  
- `cloud` (bool): If true, enables cloud-related features and will not work normally.  
- `overwrite` (bool): If true, existing audio files will be overwritten.  
- `parallel_workers` (int): Number of audio downloads/processing tasks to run in parallel.  
- `default_clip_duration_seconds` (int): Length of each trimmed audio clip.  
- `max_download_retries` (int): Number of retry attempts for failed downloads.  
- `retry_delay_seconds` (int): Delay (in seconds) between download retries.  
- `file` (string): Path to the CSV file to use for batch processing.

## Audio Settings (`audio_settings`)

- `format` (string): Output file format, such as `mp3` or `wav`.  
- `bitrate` (string): Desired bitrate for the audio output.  
- `sample_rate` (int): Target sample rate for the audio in Hz.  
- `target_dBFS` (float): Target loudness level for normalization in decibels.  
- `fade_in` / `fade_out` (bool): Whether to apply fade effects at the beginning/end.  
- `fade_in_duration_ms` / `fade_out_duration_ms` (int): Duration of fade effects in milliseconds.  
- `normalize` (bool): Whether to normalize the volume of the audio.

*Tip:* Adjust these values in the `config.json` file to suit your needs.

---

## 📑 CSV Format

| Column Header             | Purpose                                                                                     |
|---------------------------|---------------------------------------------------------------------------------------------|
| **Name**                  | The person's first name. Used for naming and identification.                               |
| **Surname**               | The person's last name. Used together with the first name for unique identification.       |
| **Song (Title & Artist)** | The full song title and artist name. This is used to search for the correct audio track.   |
| **Start Time (MM:SS)**    | The time offset in the song where the clip should start. Format must be minutes and seconds.|

---

## 🚀 Usage

1. Place your CSV file in the project folder (e.g., `~/Documents/AudioProcessingScript/playlist.csv`).  

2. Edit `config.json` to match your setup, including `csv_settings.file` and `filename_template`.  

3. Run the script:

   ```bash
   python main.py
   ```

4. (Optional) Use the Streamlit UI:

   ```bash
   streamlit run UI.py
   ```

> ⚠️ **Important Setting:**  
> The `cloud` is set to `True` by default in UI.py:

> ```python
> config["cloud"] = config.get("cloud", False)
> ```

> Change this to `False` if you want to enable the local UI.

5. View processed files in the configured output directory.

---

## 📋 Logging

- Logs are saved to the file specified in `log_filename` (default: `processes.log`)  
- Each run creates a fresh log  
- Logs include timestamps, thread info, success markers, and errors  

---

## 🤝 Support & Contribution

- Found a bug? [Open an issue](https://github.com/robertk08/AudioProcessingScript/issues)  
- Want to improve the project? Submit a pull request!  
- Questions? Contact the author or contribute via the repository.