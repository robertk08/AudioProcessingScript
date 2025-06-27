import streamlit as st
import tempfile
from pathlib import Path
from copy import deepcopy
from helpers.process_csv import process_csv
from helpers.setup import setup_logging, load_config, prepare_output_directory

# Setup
config = load_config()
config["cloud"] = config.get("cloud", True)
setup_logging(config)

st.set_page_config(page_title="🎧 Audio Studio", layout="wide")
st.title("🎧 Audio Snippet Generator")
st.markdown("A simple tool to process audio snippets from CSV files or manual input.")

st.sidebar.header("⚙️ Settings")
st.sidebar.markdown("Configure the tool behavior below:")

def config_editor_ui(cfg, prefix=""):
    updated_cfg = {}
    for key, val in cfg.items():
        if prefix == "csv_settings." and key == "file" or key == "output_dir" or key == "cloud":
            continue
        key_name = f"{prefix}{key}"
        if isinstance(val, dict):
            st.sidebar.markdown(f"**{key.replace('_', ' ').title()}**")
            updated_val = config_editor_ui(val, prefix=key_name + ".")
            updated_cfg[key] = updated_val
        elif isinstance(val, bool):
            updated_cfg[key] = st.sidebar.checkbox(key.replace('_', ' ').title(), value=val, key=key_name)
        elif isinstance(val, int):
            updated_cfg[key] = st.sidebar.number_input(key.replace('_', ' ').title(), value=val, step=1, key=key_name)
        elif isinstance(val, float):
            updated_cfg[key] = st.sidebar.number_input(key.replace('_', ' ').title(), value=val, format="%.2f", key=key_name)
        elif isinstance(val, str):
            if key == "format":
                updated_cfg[key] = st.sidebar.selectbox("Audio Format", ["mp3", "wav"], index=["mp3", "wav"].index(val), key=key_name)
            elif "dir" in key.lower() or "file" in key.lower():
                updated_cfg[key] = st.sidebar.text_input(key.replace('_', ' ').title(), value=val, key=key_name)
            else:
                updated_cfg[key] = st.sidebar.text_input(key.replace('_', ' ').title(), value=val, key=key_name)
        else:
            updated_cfg[key] = st.sidebar.text_input(key.replace('_', ' ').title(), value=str(val), key=key_name)
    return updated_cfg

config = config_editor_ui(deepcopy(config))

tab1, tab2, tab3 = st.tabs(["📄 Upload CSV", "✍️ Manual Entry", "📜 Logs"])

# Tab 1: CSV Upload
with tab1:
    st.header("📄 Upload CSV")
    st.markdown("Upload a CSV file to process multiple entries at once.")

    output_dir = config.get("output_dir", "./output")
    
    if config.get("cloud", False):
        output_dir = st.text_input(
            "📁 Output Directory",
            value=str(Path(config.get("output_dir", "./output")).expanduser()),
            help="Enter the path where processed audio files should be saved."
        )

    uploaded_csv = st.file_uploader("📂 Choose a CSV file", type="csv")

    if uploaded_csv:
        temp_csv_path = Path(tempfile.mkstemp(suffix=".csv")[1])
        with open(temp_csv_path, "wb") as f:
            f.write(uploaded_csv.read())

        if st.button("▶️ Start CSV Processing"):
            prepare_output_directory(config)
            progress = st.progress(0, text="Processing CSV...")
            st.info("⏳ Processing started...")

            process_csv(
                temp_csv_path,
                Path(output_dir).expanduser(),
                config=config,
                csv_settings=config.get("csv_settings", {}),
                audio_settings=config.get("audio_settings", {}),
                progress=progress
            )

            progress.progress(100, text="Complete")
            st.success("✅ CSV processed successfully.")

# # Tab 2: Manual Entry
# with tab2:
#     st.header("✍️ Manual Song Entry")
#     st.markdown("Enter a song manually to process it directly.")

#     col1, col2 = st.columns(2)
#     with col1:
#         first_name = st.text_input("First Name")
#         last_name = st.text_input("Last Name")
#     with col2:
#         song_query = st.text_input("YouTube Song Title or Search")
#         start_time = st.text_input("Start Time (MM:SS)", "00:00")

#     if st.button("▶️ Process Manual Entry"):
#         if not all([first_name, last_name, song_query, start_time]):
#             st.error("Please fill in all fields.")
#         else:
#             output_path = Path(config.get("output_dir", "./output")).expanduser()
#             output_path.mkdir(parents=True, exist_ok=True)

#             temp_row_path = Path(tempfile.mkstemp(suffix=".csv")[1])
#             with open(temp_row_path, "w", encoding="utf-8") as f:
#                 f.write(";".join(config["csv_settings"]["columns"].values()) + "\n")
#                 f.write(f"{first_name};{last_name};{song_query};{start_time}\n")

#             progress = st.progress(0, text="Processing Entry...")
#             st.info("⏳ Processing started...")

#             process_csv(
#                 temp_row_path,
#                 output_path,
#                 config=config,
#                 csv_settings=config.get("csv_settings", {}),
#                 audio_settings=config.get("audio_settings", {}),
#                 progress=progress
#             )

#             progress.progress(100, text="Complete")
#             st.success("✅ Manual entry processed successfully.")

# Tab 3: Logs
with tab3:
    st.header("📜 Processing Logs")
    log_file_path = Path(config.get("log_filename", "processes.log"))
    if log_file_path.exists():
        with open(log_file_path, "r", encoding="utf-8") as f:
            st.text_area("📝 Log Output", f.read(), height=400)
    else:
        st.info("No logs available.")