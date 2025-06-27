import streamlit as st
import tempfile
from pathlib import Path
from helpers.process_csv import process_csv
from helpers.setup import initialize

st.set_page_config(page_title="Audio Snippet Generator", layout="centered")
st.title("🎧 Audio Snippet Generator")

csv_file, output_dir, config, csv_settings, audio_settings = initialize()
config["zip_output"] = True
config["output_dir"] = "output"

# Minimal settings
with st.form("settings_form"):
    st.subheader("Settings")
    config["default_clip_duration_seconds"] = st.number_input(
        "Clip Length (seconds)", 1, 600, config.get("default_clip_duration_seconds", 40)
    )
    config["audio_settings"]["fade_in"] = st.checkbox(
        "Fade In", value=config["audio_settings"].get("fade_in", True)
    )
    config["audio_settings"]["fade_out"] = st.checkbox(
        "Fade Out", value=config["audio_settings"].get("fade_out", True)
    )
    config["audio_settings"]["normalize"] = st.checkbox(
        "Normalize Audio", value=config["audio_settings"].get("normalize", True)
    )
    config["audio_settings"]["format"] = st.selectbox(
        "Audio Format", ["mp3", "wav"], index=["mp3", "wav"].index(config["audio_settings"].get("format", "mp3"))
    )
    submitted = st.form_submit_button("Save Settings")

uploaded_csv = st.file_uploader("Upload CSV file", type="csv")

if uploaded_csv:
    # Save uploaded file to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_csv.read())
        temp_csv_path = tmp.name

    if st.button("Process"):
        progress = st.progress(0, text="Processing CSV...")
        try:
            process_csv(
                temp_csv_path,
                output_dir,
                config,
                csv_settings,
                audio_settings,
                progress
            )
            progress.progress(100, text="Complete")
            st.success("Processing complete!")
        except Exception as e:
            st.error(f"Error: {e}")

        zip_name = config['zip_name']+".zip"
        zip_path = output_dir / zip_name
        if zip_path.exists():
            with open(zip_path, "rb") as f:
                st.download_button(
                    label=f"Download {zip_name}",
                    data=f,
                    file_name=zip_name,
                    mime="application/zip"
                )
        else:
            st.warning("No zip file found. Check your config and try again.")


log_file = config.get("log_filename", "processes.log")
if log_file.exists():
    with open(log_file, "r", encoding="utf-8") as f:
        log_content = f.read()
        if log_content.strip():
            st.text_area("Log Output", log_content, height=300)
        else:
            st.info("Log file is empty.")
else:
    st.info("No log file found.")
       