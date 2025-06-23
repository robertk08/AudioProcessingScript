import csv
import os
import subprocess
from pydub import AudioSegment

path = os.path.expanduser("/Users/robertkrause/Documents/Projekte/Abi25Audio")
os.makedirs(path, exist_ok=True)

def timestamp_to_ms(ts):
    min, sec = map(int, ts.strip().split(":"))
    return (min * 60 + sec) * 1000

def download_song(title, filename):
    print(f"🔎 Suche und lade: {title}")
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", filename,
        f"ytsearch1:{title}"
    ]
    subprocess.run(command, check=True)

def trim_song(input_file, output_file, start_time):
    print(f"✂️ Schneide {input_file} ab {start_time}")
    audio = AudioSegment.from_file(input_file)
    start_ms = timestamp_to_ms(start_time)
    end_ms = start_ms + 30_000
    snippet = audio[start_ms:end_ms]
    snippet.export(output_file, format="mp3")

def process_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Nachname"]
            time = row["Startzeit"]
            song = row["Songtitel"]

            base_filename = os.path.join(path, f"{name}_full.%(ext)s")
            final_filename = os.path.join(path, f"{name}.mp3")

            # Song downloaden
            download_song(song, base_filename)

            # Tatsächlich heruntergeladenen Dateinamen finden
            downloaded_file = base_filename.replace("%(ext)s", "mp3")

            # Zuschneiden
            trim_song(downloaded_file, final_filename, time)

            # Ursprungsfile löschen
            os.remove(downloaded_file)

            print(f"✅ Fertig: {final_filename}")

if __name__ == "__main__":
    process_csv("daten.csv")