import streamlit as st
from detector.video_processor import VideoProcessor
from detector.model_wrapper import load_model
import tempfile
import os

st.set_page_config(page_title="Part Presence Checker", layout="wide")
st.title("🔍 Part Presence Checker")
st.markdown("Check if required car parts are present every 60 seconds in your uploaded video.")

with st.expander("📁 Upload Video File", expanded=True):
    video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

if video_file:
    st.markdown("### ⚙️ Running Detection...")

    temp_dir = tempfile.mkdtemp()
    video_path = os.path.join(temp_dir, video_file.name)
    with open(video_path, 'wb') as f:
        f.write(video_file.read())

    model = load_model("models/yolo-world.pt")
    processor = VideoProcessor(model=model, temp_dir=temp_dir)

    live_preview = st.empty()

    df, zip_path = processor.process_video(video_path, live_placeholder=live_preview)

    st.success("✅ Processing complete!")

    with st.expander("📸 Captured Frame Results", expanded=True):
        st.markdown("**Captured frames every 60 seconds with part detection status.**")
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        with open(zip_path, "rb") as f:
            st.download_button("📦 Download All Images (ZIP)", f, "results.zip", "application/zip")
    with col2:
        st.download_button("📄 Download Results Table (CSV)", data=df.to_csv(index=False), file_name="results.csv", mime="text/csv")

    st.caption("Made by Abbirami Jegan")