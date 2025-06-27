import streamlit as st
import tempfile
from helpers.process_csv import process_csv
from helpers.setup import initialize

st.title("🎧 Audio Snippet Generator")

csv_file, output_dir, config, csv_settings, audio_settings = initialize()

uploaded_csv = st.file_uploader("Upload CSV file", type="csv")

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

if uploaded_csv:
    with open("uploaded.csv", "wb") as f:
        f.write(uploaded_csv.read())

    if st.button("Process"):
        progress = st.progress(0, text="Processing CSV...")
        try:
            process_csv(
                str(uploaded_csv),
                output_dir,
                config,
                csv_settings,
                audio_settings,
                progress
            )
            progress.progress(100, text="Complete")
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