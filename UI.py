import streamlit as st
import tempfile
from pathlib import Path
from Script import process_csv, config, setup_logging  # Adjust import if your script filename differs

progress = None
status_msg = st.empty()

# Set up logging
setup_logging()

st.set_page_config(page_title="🎧 Audio Studio", layout="centered", initial_sidebar_state="expanded")

# Sidebar – runtime config (will override config.json temporarily)
st.sidebar.title("⚙️ Configuration")
audio_format = st.sidebar.selectbox("Audio Format", ["mp3", "wav", "aac"], index=["mp3", "wav", "aac"].index(config.get("audio_format", "mp3")))
clip_duration = st.sidebar.slider("Clip Duration (seconds)", 10, 120, config.get("default_clip_duration_seconds", 40))
normalize = st.sidebar.checkbox("Normalize Audio", value=config.get("normalize_audio", True))
fade_in = st.sidebar.checkbox("Fade In", value=config.get("fade_in", False))
fade_out = st.sidebar.checkbox("Fade Out", value=config.get("fade_out", False))
sample_rate = st.sidebar.selectbox("Sample Rate", [None, 44100, 48000], index=[None, 44100, 48000].index(config.get("sample_rate", 44100)))
target_dBFS = st.sidebar.slider("Target dBFS", -40.0, 0.0, config.get("target_dBFS", -20.0))

# UI title
st.title("🎵 Audio Snippet Generator")

# Tabs
tabs = st.tabs(["📄 Upload CSV", "✍️ Manual Entry", "🧩 Settings", "📜 Logs"])

# Output directory
output_dir = Path(config.get("output_dir", "./output")).expanduser()
output_dir.mkdir(parents=True, exist_ok=True)

# Helper to update runtime config
def update_runtime_config():
    config["audio_format"] = audio_format
    config["default_clip_duration_seconds"] = clip_duration
    config["normalize_audio"] = normalize
    config["fade_in"] = fade_in
    config["fade_out"] = fade_out
    config["sample_rate"] = sample_rate
    config["target_dBFS"] = target_dBFS

# === Tab 1: Upload CSV ===
with tabs[0]:
    st.subheader("Upload CSV File")
    uploaded_csv = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_csv:
        temp_csv_path = Path(tempfile.mkstemp(suffix=".csv")[1])
        with open(temp_csv_path, "wb") as f:
            f.write(uploaded_csv.read())

        if st.button("Start CSV Processing"):
            update_runtime_config()
            progress = st.progress(0, text="Processing CSV...")
            status_msg.info("⏳ Starting CSV processing...")
            process_csv(temp_csv_path, output_dir, progress=progress)
            progress.progress(100, text="Complete")
            status_msg.success("✅ CSV processed successfully.")

# === Tab 2: Manual Entry ===
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
            update_runtime_config()
            temp_row_path = Path(tempfile.mkstemp(suffix=".csv")[1])
            with open(temp_row_path, "w", encoding="utf-8") as f:
                f.write(";".join(config["csv_columns"].values()) + "\n")
                f.write(f"{first_name};{last_name};{song_query};{start_time}\n")
            progress = st.progress(0, text="Processing Entry...")
            status_msg.info("⏳ Starting manual entry processing...")
            process_csv(temp_row_path, output_dir, progress=progress)
            progress.progress(100, text="Complete")
            status_msg.success("✅ Manual entry processed successfully.")

# === Tab 3: Settings Overview ===
with tabs[2]:
    st.subheader("🧩 Runtime Settings")
    st.json(config)

# === Tab 4: Log Viewer ===
with tabs[3]:
    st.subheader("📜 Logs")
    log_file = Path(config.get("log_file", "processes.log"))
    if log_file.exists():
        with open(log_file, "r", encoding="utf-8") as f:
            st.text_area("Log Output", f.read(), height=300)
    else:
        st.info("No logs yet.")