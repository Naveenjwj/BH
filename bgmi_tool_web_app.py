import streamlit as st
import pandas as pd
from pytube import YouTube
import cv2
import os

st.title("BGMI Tool – YouTube Frame Extractor")

yt_url = st.text_input("Paste YouTube URL here:")
uploaded_csv = st.file_uploader("Upload Timestamp CSV (hh:mm:ss, team, map)", type="csv")

if yt_url and uploaded_csv:
    try:
        # Save uploaded CSV
        df = pd.read_csv(uploaded_csv, header=None, names=["time", "team", "map"])

        # Download video
        st.write("📥 Downloading YouTube video...")
        yt = YouTube(yt_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video_path = stream.download(output_path="data/videos")

        # Extract frames
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)

        for index, row in df.iterrows():
            h, m, s = map(int, row['time'].split(":"))
            sec = h * 3600 + m * 60 + s
            frame_no = int(sec * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            if ret:
                out_dir = f"data/frames/{row['map']}/{row['team']}"
                os.makedirs(out_dir, exist_ok=True)
                filename = f"{row['time'].replace(':', '-')}.jpg"
                cv2.imwrite(os.path.join(out_dir, filename), frame)
        
        cap.release()
        st.success("✅ Frames extracted successfully.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
