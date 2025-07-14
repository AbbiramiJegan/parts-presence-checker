import cv2
import os
import pandas as pd
import zipfile
from .utils import resize_frame, draw_boxes, encode_image_to_base64

class VideoProcessor:
    CLASS_NAMES = [
        'arm rest', 'clip door trim', 'door trim', 'front assist grip',
        'inner brush', 'inner handle', 'outer mirror inner cover',
        'screw inner handle', 'weather strip door'
    ]
    TARGET_CLASSES = {'weather strip door'}
    CAPTURE_INTERVAL = 3

    def __init__(self, model, temp_dir):
        self.model = model
        self.temp_dir = temp_dir
        self.save_dir = os.path.join(temp_dir, "frames")
        os.makedirs(self.save_dir, exist_ok=True)

    def process_video(self, video_path, live_placeholder=None):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * self.CAPTURE_INTERVAL)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        frame_count = 0
        image_index = 0
        results_data = []

        import streamlit as st
        progress_bar = st.progress(0)

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            frame = resize_frame(frame)

            if frame_count == 0 or frame_count % frame_interval == 0:
                result = self.model(frame, conf=0.4, iou=0.4)[0]
                detected_classes, annotated_frame = draw_boxes(result, frame, self.CLASS_NAMES, self.TARGET_CLASSES)

                status = "OK" if self.TARGET_CLASSES.issubset(detected_classes) else "NG"
                emoji = "✅" if status == "OK" else "❌"
                filename = f"frame_{image_index:03d}_{status}.jpg"
                filepath = os.path.join(self.save_dir, filename)
                cv2.imwrite(filepath, annotated_frame)

                img_b64 = encode_image_to_base64(annotated_frame)
                results_data.append({
                    "Time": f"{frame_count // fps:.0f}s",
                    "Status": f"{status} {emoji}",
                    "Image": f'<img src="data:image/jpeg;base64,{img_b64}" width="1000">',
                    "Detected Components": ", ".join(sorted(detected_classes)) if detected_classes else "None"
                })

                if live_placeholder:
                    from PIL import Image
                    import io
                    pil_img = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
                    live_placeholder.image(pil_img, caption=f"Time: {frame_count // fps:.0f}s | Status: {status}", width=800)

                image_index += 1

            frame_count += 1
            progress_bar.progress(min(int((frame_count / total_frames) * 100), 100))

        cap.release()
        progress_bar.empty()

        df = pd.DataFrame(results_data)

        zip_path = os.path.join(self.temp_dir, "results.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in os.listdir(self.save_dir):
                zipf.write(os.path.join(self.save_dir, file), arcname=file)

        return df, zip_path
