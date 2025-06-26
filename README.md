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
- `output_dir` (string): Directory where the processed clips will be saved. Supports tilde (`~`) for home directory.
- `log_filename` (string): Name of the file where logs will be written.
- `filename_template` (string): Template for output filenames using placeholders `{1}`, `{2}`, `{3}` for `name`, `surname`, and `song` respectively.
- `cloud` (bool): If true, enables cloud-related features (currently not enabled by default).
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
- `file` (string): Path to the CSV file to use for batch processing.
- `delimiter` (string): Character used to separate columns in the CSV.
- `columns` (object): Mapping of expected column keys to the headers used in your CSV:
  - `name`: Column in the csv file that describes the person’s first name  
  - `surname`: Column in the csv file that describes the person’s last name  
  - `song`: column in the csv file that describes the song entry (title & artist)  
  - `start_time`: column in the csv file that describes where in the song to begin clipping (in MM:SS format)

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

1. Place your CSV file in the project directory (e.g., `~/Documents/AudioProcessingScript/playlist.csv`).  
2. Edit `config.json` to set your preferences, including the path to the CSV file and filename template.  
3. Run the script:
   ```bash
   python Script.py
   ```
4. (Optional) Launch the Streamlit interface:
   ```bash
   streamlit run UI.py
   ```
5. Use the web interface to select your CSV and configure the run interactively.  
6. Check the output directory (as set in `output_dir`) for processed clips.

## Logging

- Progress and errors are logged to the file specified in `log_filename` (default: `processes.log`).  
- Each run clears the previous log, so you start with a fresh log on every execution.  
- Logs include detailed timestamps, thread information, and success/failure markers for easier debugging and tracking.

## Support & Contribution

Feel free to open issues or submit pull requests on the project repository. For questions, contact the author.
# 🎧 Audio Processing Script

A Python-based tool to automate downloading, trimming, and exporting audio clips from YouTube based on a customizable CSV playlist. Includes a beautiful Streamlit UI for easy use.

---

## 📚 Table of Contents

1. [✨ Features](#-features)  
2. [🧰 Requirements](#-requirements)  
3. [⚙️ Installation](#-installation)  
4. [🛠️ Configuration](#-configuration)  
5. [📑 CSV Format](#-csv-format)  
6. [🚀 Usage](#-usage)  
7. [📋 Logging](#-logging)  
8. [🤝 Support & Contribution](#-support--contribution)

---

## ✨ Features

- 🔍 Search & download audio from YouTube  
- ✂️ Trim clips using precise start times  
- ⚙️ Fully configurable: format, bitrate, fade durations, loudness, etc.  
- 🎧 Audio processing: normalization, fade in/out, silence trimming  
- 💽 Export in MP3/WAV/FLAC with custom filename templates  
- 🧵 Multi-threaded: up to 15 parallel tasks  
- 📄 Flexible CSV column mapping  
- 🖥️ Streamlit-based interactive UI  
- 📊 Visual progress bars and real-time status  
- 📝 Structured logging for each processing run

---

## 🧰 Requirements

- Python 3.7+  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)  
- [pydub](https://github.com/jiaaro/pydub)  
- [tqdm](https://github.com/tqdm/tqdm)  
- [streamlit](https://streamlit.io/)  
- [ffmpeg](https://ffmpeg.org/) installed and in your system `PATH`  

All Python packages are listed in `requirements.txt`.

---

## ⚙️ Installation

1. **Install Python** (if not already available).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Install ffmpeg**:
   - macOS: `brew install ffmpeg`
   - Windows: Download from https://ffmpeg.org/download.html and add it to `PATH`.

---

## 🛠️ Configuration

All settings are stored in `config.json`. Main sections:

### 🔧 General
- `output_dir`: Where processed audio files are saved. Supports tilde (`~`) for home directory.  
- `log_filename`: Log file name  
- `filename_template`: Customize output filenames using placeholders `{1}`, `{2}`, `{3}` for `name`, `surname`, and `song` respectively, e.g. `"{2}_{1}_{3}"` results in `Miller_Lena_Imagine Dragons - Believer.mp3`  
- `cloud`: Enable cloud-related features (default: false)  
- `overwrite`: Whether to overwrite existing files  
- `parallel_workers`: Number of concurrent jobs  
- `default_clip_duration_seconds`: Default clip length  
- `max_download_retries`: Download retry attempts  
- `retry_delay_seconds`: Delay between retries  

### 🎛️ Audio Settings (`audio_settings`)
- `format`: `mp3`, `wav`, `flac`, etc.  
- `bitrate`: e.g., `"320k"`  
- `sample_rate`: Sample rate in Hz  
- `target_dBFS`: Normalization level  
- `fade_in`, `fade_out`: Enable fade effects  
- `fade_in_duration_ms`, `fade_out_duration_ms`: Fade durations  
- `normalize`: Whether to normalize volume  

### 📂 CSV Settings (`csv_settings`)
- `file`: Path to input CSV file  
- `delimiter`: CSV delimiter (e.g., `;` or `,`)  
- `columns`: Mapping from expected fields to CSV headers:
  - `name`: First name  
  - `surname`: Last name  
  - `song`: Song title & artist  
  - `start_time`: Start time (in `MM:SS`)  

---

## 📑 CSV Format

The input CSV should have headers matching the keys set in `csv_settings.columns`. For example:

```csv
Name;Surname;Song (Title & Artist);Start Time (Minutes:Seconds)
Lena;Miller;Imagine Dragons - Believer;00:23
```

### Explanation of CSV Columns:

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