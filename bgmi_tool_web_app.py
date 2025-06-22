# bgmi_tool_web_app.py

import streamlit as st
import pandas as pd
import os
import cv2

st.title("🎮 BGMI Match Video Frame Extractor")

# Upload video
uploaded_video = st.file_uploader("📤 Upload Match Video (.mp4)", type=["mp4"])

# Upload CSV
uploaded_csv = st.file_uploader("📄 Upload Timestamp CSV (hh:mm:ss, team, map)", type=["csv"])

if uploaded_video and uploaded_csv:
    # Save video
    os.makedirs("data/videos", exist_ok=True)
    video_path = os.path.join("data/videos", uploaded_video.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_video.read())
    
    # Load CSV
    df = pd.read_csv(uploaded_csv, header=None, names=["time", "team", "map"])
    st.success("✅ CSV and Video Uploaded Successfully")

    # Extract frames
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    with st.spinner("⏳ Extracting frames..."):
        for _, row in df.iterrows():
            try:
                h, m, s = map(int, row["time"].split(":"))
                frame_no = int((h * 3600 + m * 60 + s) * fps)
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
                ret, frame = cap.read()
                if ret:
                    out_dir = f"data/frames/{row['map']}/{row['team']}"
                    os.makedirs(out_dir, exist_ok=True)
                    fname = f"{row['time'].replace(':', '-')}.jpg"
                    cv2.imwrite(os.path.join(out_dir, fname), frame)
            except Exception as e:
                st.error(f"Error at {row['time']}: {e}")

        cap.release()
        st.success("✅ All frames extracted and saved to folders.")

else:
    st.info("⬆ Upload both video and CSV to begin.")
