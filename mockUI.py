import streamlit as st

st.set_page_config(page_title="Audio Processor", layout="wide")

# Sidebar: Global settings
st.sidebar.title("⚙️ Configuration")
audio_format = st.sidebar.selectbox("Audio Format", ["mp3", "wav", "aac"], index=0)
clip_duration = st.sidebar.slider("Clip Duration (seconds)", 10, 120, 30)
normalize = st.sidebar.checkbox("Normalize Audio", value=True)
fade_in = st.sidebar.checkbox("Fade In")
fade_out = st.sidebar.checkbox("Fade Out")
sample_rate = st.sidebar.selectbox("Sample Rate", [None, 44100, 48000], index=1)
target_dBFS = st.sidebar.slider("Target dBFS", -40.0, 0.0, -20.0)

# Title
st.title("🎵 Audio Snippet Generator")

# Tabs for different modes
tabs = st.tabs(["📄 Upload CSV", "✍️ Manual Entry", "🧩 Settings", "📜 Logs"])

# Tab 1: Upload CSV
with tabs[0]:
    st.subheader("Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file:
        st.success("CSV uploaded!")
        st.button("Start Processing")
        st.progress(0)  # Placeholder

# Tab 2: Manual Entry
with tabs[1]:
    st.subheader("Enter Track Details")
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
    with col2:
        song_query = st.text_input("Song Title / YouTube Search")
        start_time = st.text_input("Start Time (MM:SS)", "00:00")

    if st.button("Process This Entry"):
        st.info("This is where processing would start...")

# Tab 3: Settings Display (future: config editor)
with tabs[2]:
    st.subheader("🛠 Current Settings")
    st.json({
        "audio_format": audio_format,
        "clip_duration": clip_duration,
        "normalize_audio": normalize,
        "fade_in": fade_in,
        "fade_out": fade_out,
        "sample_rate": sample_rate,
        "target_dBFS": target_dBFS,
    })

# Tab 4: Log Output
with tabs[3]:
    st.subheader("🔍 Log Output")
    st.text_area("Logs", "No logs yet...", height=200)