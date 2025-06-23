# Abi25 Audio Script

Dieses Skript lädt Songs aus einer CSV-Datei herunter, schneidet sie und speichert sie als Audiodateien.

## Vorbereitung

1. Installiere Python, falls noch nicht vorhanden.
2. Installiere `yt-dlp` mit folgendem Befehl:

```bash
pip install yt-dlp
```

3. Installiere `pydub`, z. B. mit:

```bash
pip install pydub
```

4. Installiere `ffmpeg`:
   - **macOS (mit Homebrew):**

     ```bash
     brew install ffmpeg
     ```

   - **Windows:**
     - Lade FFmpeg von [ffmpeg.org](https://ffmpeg.org/download.html) herunter.
     - Entpacke es und füge den `bin`-Ordner zu deiner Systemumgebungsvariable `PATH` hinzu.

## Verwendung

1. Passe die Datei `config.json` an (z. B. welcher Ordner genutzt wird, welches Dateiformat, welche CSV-Datei).
2. Lege deine CSV-Datei (z. B. `testdata.csv`) in das Projektverzeichnis.
3. Starte das Skript:

```bash
python Script.py
```

Das Skript lädt die Songs, schneidet sie ab einer bestimmten Startzeit und speichert sie als Datei.

## Hinweise

- Die Startzeit muss im Format `MM:SS` angegeben sein (z. B. `00:30`).
- Die Ergebnisse findest du im in der Config angegebenen Ordner.
- Fehler und Fortschritt werden in der Datei `process_log.txt` gespeichert.