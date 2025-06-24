import streamlit as st
import tempfile
import json
from pathlib import Path
from copy import deepcopy
from helpers.process_csv import process_csv
from helpers.setup import setup_logging, load_config

# Load and setup
config = load_config()
setup_logging(config)

st.set_page_config(page_title="🎧 Audio Studio", layout="centered")

status_msg = st.empty()
progress = None

st.title("🎵 Audio Snippet Generator")

tabs = st.tabs(["📄 Upload CSV", "✍️ Manual Entry", "⚙️ Settings", "📜 Logs"])

def config_editor_ui(cfg, prefix=""):
    updated_cfg = {}
    for key, val in cfg.items():
        # Skip CSV input file setting since it's handled in the Upload CSV tab
        if prefix == "csv_settings." and key == "file" or key == "output_dir" :
            continue
        key_name = f"{prefix}{key}"
        if isinstance(val, dict):
            st.markdown(f"### {key.replace('_', ' ').title()}")
            updated_val = config_editor_ui(val, prefix=key_name + ".")
            updated_cfg[key] = updated_val
        elif isinstance(val, bool):
            updated_cfg[key] = st.checkbox(key.replace('_', ' ').title(), value=val, key=key_name)
        elif isinstance(val, int):
            updated_cfg[key] = st.number_input(key.replace('_', ' ').title(), value=val, step=1, key=key_name)
        elif isinstance(val, float):
            updated_cfg[key] = st.number_input(key.replace('_', ' ').title(), value=val, format="%.2f", key=key_name)
        elif isinstance(val, str):
            # Special case for audio format - restrict choices to wav and mp3
            if key == "format":
                updated_cfg[key] = st.selectbox("Audio Format", ["mp3", "wav"], index=["mp3", "wav"].index(val), key=key_name)
            elif "dir" in key.lower() or "file" in key.lower():
                # File path input
                updated_cfg[key] = st.text_input(key.replace('_', ' ').title(), value=val, key=key_name)
            else:
                updated_cfg[key] = st.text_input(key.replace('_', ' ').title(), value=val, key=key_name)
        else:
            # Fallback: show as text input
            updated_cfg[key] = st.text_input(key.replace('_', ' ').title(), value=str(val), key=key_name)
    return updated_cfg

with tabs[0]:
    
    import os  # add this at the top of your file

    st.markdown("### Output Directory")
    output_dir = st.text_input(
        "Enter output folder path",
        value=str(Path(config.get("output_dir", "./output")).expanduser()),
        help="Paste or type the path to the folder where audio files will be saved"
    )

    if not os.path.isdir(output_dir):
        st.warning("⚠️ The provided path does not exist or is not a directory.")
   
    uploaded_csv = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_csv:
        temp_csv_path = Path(tempfile.mkstemp(suffix=".csv")[1])
        with open(temp_csv_path, "wb") as f:
            f.write(uploaded_csv.read())

        if st.button("Start CSV Processing"):
            output_path = Path(output_dir).expanduser()
            output_path.mkdir(parents=True, exist_ok=True)

            progress = st.progress(0, text="Processing CSV...")
            status_msg.info("⏳ Starting CSV processing...")

            # Pass edited config down or parts of it if needed in process_csv
            process_csv(temp_csv_path, output_path, progress=progress)

            progress.progress(100, text="Complete")
            status_msg.success("✅ CSV processed successfully.")

with tabs[1]:
    st.subheader("Manual Song Entry")
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
    with col2:
        song_query = st.text_input("YouTube Song Title or Search")
        start_time = st.text_input("Start Time (MM:SS)", "00:00")

    if st.button("Process Entry"):
        if not all([first_name, last_name, song_query, start_time]):
            st.error("Please fill in all fields.")
        else:
            output_path = Path(edited_config.get("output_dir", "./output")).expanduser()
            output_path.mkdir(parents=True, exist_ok=True)

            temp_row_path = Path(tempfile.mkstemp(suffix=".csv")[1])
            with open(temp_row_path, "w", encoding="utf-8") as f:
                f.write(";".join(edited_config["csv_settings"]["columns"].values()) + "\n")
                f.write(f"{first_name};{last_name};{song_query};{start_time}\n")

            progress = st.progress(0, text="Processing Entry...")
            status_msg.info("⏳ Starting manual entry processing...")

            process_csv(temp_row_path, output_path, progress=progress)

            progress.progress(100, text="Complete")
            status_msg.success("✅ Manual entry processed successfully.")

with tabs[2]:
    st.subheader("⚙️ Configuration Editor (all options editable)")

    # Deepcopy config so we can edit safely
    edited_config = config_editor_ui(deepcopy(config))

    st.markdown("---")
    st.subheader("📄 Current Configuration (auto-updated)")

    # Show updated config JSON pretty-printed
    st.json(edited_config)

with tabs[3]:
    st.subheader("📜 Logs")
    log_file_path = Path(edited_config.get("log_filename", "processes.log"))
    if log_file_path.exists():
        with open(log_file_path, "r", encoding="utf-8") as f:
            st.text_area("Log Output", f.read(), height=300)
    else:
        st.info("No logs yet.")