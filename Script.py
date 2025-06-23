import csv
import os
import subprocess
from pydub import AudioSegment

output_dir = os.path.expanduser("/Users/robertkrause/Documents/Projekte/Abi25Audio")
os.makedirs(output_dir, exist_ok=True)

def timestamp_to_ms(ts):
    try:
        min, sec = map(int, ts.strip().split(":"))
        return (min * 60 + sec) * 1000
    except Exception:
        return None

def download_song(query, temp_path):
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", temp_path,
        f"ytsearch1:{query}"
    ]
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def trim_song(input_path, output_path, start_time):
    start_ms = timestamp_to_ms(start_time)
    if start_ms is None:
        print(f"❌ Ungültige Startzeit: {start_time}")
        return False
    try:
        audio = AudioSegment.from_file(input_path)
        end_ms = start_ms + 30_000
        snippet = audio[start_ms:end_ms]
        snippet.export(output_path, format="mp3")
        return True
    except Exception as e:
        print(f"❌ Fehler beim Schneiden: {e}")
        return False

def process_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')  # Semikolon als Trenner
        for row in reader:
            vorname = row["Name"].strip()
            nachname = row["Nachname"].strip()
            song = row["Lied (Titel & Künstler)"].strip()
            startzeit = row["Startzeit (Minute/Sekunde)"].strip()

            if not vorname or not nachname or not song or not startzeit:
                continue  # Zeile überspringen

            filename_base = f"{nachname}, {vorname}"
            temp_path = os.path.join(output_dir, f"{filename_base}_full.%(ext)s")
            final_path = os.path.join(output_dir, f"{filename_base}.mp3")

            print(f"🔄 Verarbeite {vorname} {nachname}: {song} ab {startzeit}")

            if not download_song(song, temp_path):
                print(f"❌ Download fehlgeschlagen für {song}")
                continue

            downloaded_file = temp_path.replace("%(ext)s", "mp3")
            if not trim_song(downloaded_file, final_path, startzeit):
                continue

            if os.path.exists(downloaded_file):
                os.remove(downloaded_file)

            print(f"✅ Gespeichert: {final_path}")

if __name__ == "__main__":
    process_csv("testdata.csv")