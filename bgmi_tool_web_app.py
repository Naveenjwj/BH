# bgmi_tool_web_app.py (Streamlit version)
import streamlit as st
import pandas as pd
import os
import csv
import cv2
from pytube import YouTube

st.set_page_config(page_title="BGMI Heatmap Tool", layout="centered")
st.title("📍 BGMI Heatmap & Frame Extractor Tool")

# Input YouTube Link
yt_link = st.text_input("🎥 Enter YouTube Link")

# Upload timestamp CSV
csv_file = st.file_uploader("📁 Upload Timestamp CSV (hh:mm:ss, team, map)", type=["csv"])

process_btn = st.button("🚀 Process Video and Extract Frames")

if process_btn and yt_link and csv_file:
    try:
        # Download YouTube video
        st.info("⏬ Downloading video...")
        yt = YouTube(yt_link)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        filename = stream.download(output_path="data/videos")

        st.success(f"✅ Video downloaded: {yt.title}")

        # OpenCV process
        cap = cv2.VideoCapture(filename)
        fps = cap.get(cv2.CAP_PROP_FPS)

        df = pd.read_csv(csv_file, header=None)
        st.info("📸 Extracting frames...")
        progress_bar = st.progress(0)

        for idx, row in df.iterrows():
            timestamp_str, team, map_name = row
            h, m, s = map(int, timestamp_str.split(':'))
            total_sec = h * 3600 + m * 60 + s
            frame_number = int(total_sec * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            if ret:
                out_dir = f"data/frames/{map_name}/{team}"
                os.makedirs(out_dir, exist_ok=True)
                out_path = os.path.join(out_dir, f"{timestamp_str.replace(':', '-')}.jpg")
                cv2.imwrite(out_path, frame)

            progress_bar.progress((idx + 1) / len(df))

        cap.release()
        st.success("✅ All frames extracted and saved successfully.")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

elif process_btn:
    st.warning("⚠️ Please provide both YouTube link and CSV file.")


