import streamlit as st
from yt_dlp import YoutubeDL
import os

st.set_page_config(page_title="YouTube Downloader", layout="centered")
st.title("YouTube Downloader")
st.write("Download YouTube videos as MP3 or MP4!")

url = st.text_input("Enter the YouTube URL:")

if url:
    try:
        with YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            st.write(f"**Title:** {info['title']}")
            st.write(f"**Views:** {info['view_count']}")
            st.write(f"**Duration:** {info['duration']} seconds")

            download_type = st.radio("Select download type:", ("Video (MP4)", "Audio (MP3)"))

            if download_type == "Video (MP4)":
                formats = [f"{f['format']} ({f['format_note']})" for f in info['formats'] if f['ext'] == 'mp4']
                selected_format = st.selectbox("Select video quality:", formats)

                format_id = info['formats'][formats.index(selected_format)]['format_id']
            else:
                format_id = "bestaudio"

            if st.button("Download"):
                with st.spinner("Downloading..."):
                    download_path = os.path.join(os.getcwd(), "downloads")
                    os.makedirs(download_path, exist_ok=True)
                    ydl_opts = {
                        'format': format_id,
                        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                        'http_headers': {
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                                        'Accept-Language': 'en-US,en;q=0.9',
                                        },
                    }

                    with YoutubeDL(ydl_opts) as ydl_download:
                        result = ydl_download.download([url])
                    
                    st.success(f"Download completed! File saved to: `{download_path}`")
    except Exception as e:
        st.error(f"An error occurred: {e}")
