# bgmi_tool_web_app.py (Streamlit version)
import streamlit as st
import os
import csv
from pytube import YouTube
import cv2
from io import StringIO
import numpy as np
import base64

st.set_page_config(page_title="BGMI Zone Analyzer", layout="wide")
st.title("📍 BGMI Heatmap & Safe Zone Analyzer")

st.sidebar.header("Upload Inputs")

# --- YouTube Input & CSV Timestamp ---
yt_url = st.sidebar.text_input("YouTube Match Link")
csv_file = st.sidebar.file_uploader("Upload Timestamp CSV (hh:mm:ss, team, map)", type=['csv'])

if st.sidebar.button("Process YouTube") and yt_url and csv_file:
    try:
        yt = YouTube(yt_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        filename = stream.download(output_path="data/videos")
        
        cap = cv2.VideoCapture(filename)
        fps = cap.get(cv2.CAP_PROP_FPS)

        stringio = StringIO(csv_file.getvalue().decode("utf-8"))
        reader = csv.reader(stringio)

        for row in reader:
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

        cap.release()
        st.success("Video processed and frames saved!")

    except Exception as e:
        st.error(f"Error: {str(e)}")

# --- Simulate Zones ---
st.header("📊 Zone Simulator")
map_name = st.selectbox("Select Map", ["erangel", "miramar", "sanhok"])

# Load available teams
temp_dir = f"data/frames/{map_name}"
teams = sorted(os.listdir(temp_dir)) if os.path.exists(temp_dir) else []
selected_teams = st.multiselect("Select Teams", teams)
num_zones = st.slider("Number of Simulated Zones", min_value=1, max_value=200, value=100)

if st.button("Simulate & Recommend Safe Zones"):
    st.info("Running simulation (mock output)...")

    # Placeholder for simulation logic
    heatmap = np.random.rand(256, 256)
    st.image(heatmap, caption="Simulated Zone Heatmap", use_column_width=True, clamp=True)

# --- Report Generator ---
st.header("🧾 Export Zone Report")
if st.button("Export PDF Report"):
    st.warning("This feature is under development.")
