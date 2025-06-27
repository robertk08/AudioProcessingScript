# app.py
import streamlit as st
from yt_dlp import YoutubeDL
import tempfile
import os

st.title("Video Downloader with yt-dlp (No Cookies)")

url = st.text_input("Enter video URL")
if st.button("Download"):
    if not url:
        st.error("Please enter a URL.")
        st.stop()

    # create a temp directory for download
    tmp_dir = tempfile.mkdtemp()
    out_template = os.path.join(tmp_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": out_template,
        # no cookies
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        },
        "noprogress": True,
        "quiet": True,
    }

    with st.spinner("Downloading..."):
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
        except Exception as e:
            st.error(f"Download failed: {e}")
            st.stop()

    # prepare filename and offer download
    filename = ydl.prepare_filename(info)
    st.success(f"Downloaded: {os.path.basename(filename)}")
    with open(filename, "rb") as f:
        st.download_button(
            label="Click to download video",
            data=f,
            file_name=os.path.basename(filename),
            mime="video/mp4"
        )