import csv
import json
import os
import subprocess
import time
import logging
from pydub import AudioSegment

# Config laden
def load_config(path="config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()

log_file = config.get("log_file", "process_log.txt")

# Logdatei zu Beginn leeren
with open(log_file, "w", encoding="utf-8") as f:
    f.write("")

# Logging konfigurieren
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

output_dir = os.path.expanduser(config.get("output_dir", "./output"))
os.makedirs(output_dir, exist_ok=True)

def timestamp_to_ms(ts):
    try:
        min_, sec = map(int, ts.strip().split(":"))
        return (min_ * 60 + sec) * 1000
    except Exception as e:
        logging.error(f"Ungültige Startzeit '{ts}': {e}")
        return None

def download_song(query, temp_path, retries=3, delay=5):
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", config.get("audio_format", "mp3"),
        "-o", temp_path,
        f"ytsearch1:{query}"
    ]
    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Versuche Download: '{query}', Versuch {attempt}")
            subprocess.run(command, check=True)
            return True
        except subprocess.CalledProcessError as e:
            logging.warning(f"Downloadversuch {attempt} fehlgeschlagen: {e}")
            if attempt < retries:
                time.sleep(delay)
    return False

def trim_song(input_path, output_path, start_time, duration_sec=30, normalize=True):
    start_ms = timestamp_to_ms(start_time)
    if start_ms is None:
        logging.error(f"Ungültige Startzeit: {start_time}")
        return False
    try:
        audio = AudioSegment.from_file(input_path)
        end_ms = start_ms + duration_sec * 1000
        if end_ms > len(audio):
            end_ms = len(audio)
        snippet = audio[start_ms:end_ms]
        if normalize:
            snippet = match_target_amplitude(snippet, -20.0)
        # Nutze Format aus Config (Standard mp3)
        audio_format = config.get("audio_format", "mp3")
        snippet.export(output_path, format=audio_format)
        return True
    except Exception as e:
        logging.error(f"Fehler beim Schneiden: {e}")
        return False

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def process_csv(csv_path):
    delimiter = config.get("csv_delimiter", ";")
    with open(csv_path, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        for row in reader:
            vorname = row.get("Name", "").strip()
            nachname = row.get("Nachname", "").strip()
            song = row.get("Lied (Titel & Künstler)", "").strip()
            startzeit = row.get("Startzeit (Minute/Sekunde)", "").strip()

            if not vorname or not nachname or not song or not startzeit:
                logging.info(f"Überspringe unvollständige Zeile: {row}")
                continue

            filename_base = f"{nachname}, {vorname}"
            audio_format = config.get("audio_format", "mp3")
            final_path = os.path.join(output_dir, f"{filename_base}.{audio_format}")
            temp_path = os.path.join(output_dir, f"{filename_base}_full.%(ext)s")

            if os.path.exists(final_path) and not config.get("overwrite_existing_files", False):
                logging.info(f"Datei existiert bereits und overwrite ist False: {final_path}")
                print(f"⏭ Überspringe {filename_base}, Datei existiert.")
                continue

            print(f"🔄 Verarbeite {vorname} {nachname}: {song} ab {startzeit}")
            logging.info(f"Starte Verarbeitung: {vorname} {nachname}, Song: {song}, Startzeit: {startzeit}")

            if not download_song(song, temp_path,
                                 retries=config.get("max_download_retries", 3),
                                 delay=config.get("retry_delay_seconds", 5)):
                logging.error(f"Download fehlgeschlagen für {song}")
                print(f"❌ Download fehlgeschlagen für {song}")
                continue

            downloaded_file = temp_path.replace("%(ext)s", audio_format)

            if not trim_song(downloaded_file, final_path, startzeit,
                             duration_sec=config.get("default_clip_duration_seconds", 30),
                             normalize=config.get("normalize_audio", True)):
                logging.error(f"Schneiden fehlgeschlagen für {final_path}")
                print(f"❌ Schneiden fehlgeschlagen für {final_path}")
                continue

            if os.path.exists(downloaded_file):
                os.remove(downloaded_file)

            print(f"✅ Gespeichert: {final_path}")
            logging.info(f"Erfolgreich gespeichert: {final_path}")

if __name__ == "__main__":
    csv_file = config.get("csv_file", "testdata.csv")
    process_csv(csv_file)