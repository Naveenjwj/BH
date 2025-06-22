import streamlit as st
from pytube import YouTube
import cv2
import os
import pandas as pd
import datetime

st.set_page_config(page_title="BGMI Zone Tool", layout="centered")

st.title("📍 BGMI Zone Strategy Tool")

# --- YouTube and CSV Input ---
st.header("🎥 YouTube Match Import")

yt_url = st.text_input("Enter YouTube Video URL")
csv_file = st.file_uploader("Upload CSV (hh:mm:ss, team, map):", type=["csv"])

process = st.button("Process Video & Extract Frames")

if process:
    if not yt_url or not csv_file:
        st.error("Please provide both YouTube URL and CSV file.")
    else:
        try:
            with st.spinner("📥 Downloading YouTube video..."):
                yt = YouTube(yt_url)
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                filename = stream.download(output_path="data/videos")

            cap = cv2.VideoCapture(filename)
            fps = cap.get(cv2.CAP_PROP_FPS)

            df = pd.read_csv(csv_file, header=None, names=["time", "team", "map"])
            for _, row in df.iterrows():
                time_str, team, map_name = row
                h, m, s = map(int, time_str.strip().split(":"))
                total_sec = h * 3600 + m * 60 + s
                frame_number = int(total_sec * fps)
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                ret, frame = cap.read()
                if ret:
                    out_dir = f"data/frames/{map_name}/{team}"
                    os.makedirs(out_dir, exist_ok=True)
                    out_path = os.path.join(out_dir, f"{time_str.replace(':', '-')}.jpg")
                    cv2.imwrite(out_path, frame)

            cap.release()
            st.success("✅ Frames extracted and saved!")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
