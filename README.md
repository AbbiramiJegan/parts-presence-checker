## Part Presence Checker (YOLO + Streamlit)

A Streamlit-based web application that checks for the presence of specific car parts in uploaded video files using YOLO object detection.

## Demo

 - Upload a video and automatically:
   
 - Extract frames every N seconds
 
 - Run YOLOv8 object detection

 - Check if required car parts are present
   
 - Display and download annotated frames + detection report

## Model Support

**This app works with both:**

Pretrained YOLO models (e.g., yolov8n.pt)

Custom-trained YOLO models (like your own)

**Simply change the path in the code:**

model = YOLO("your_model.pt")

This repo was built using a custom YOLO model trained to detect specific car parts.

## Supported Labels (Custom Model)

The following labels are supported by the custom model used in this project:

    arm rest
    clip door trim
    door trim
    front assist grip
    inner brush
    inner handle
    outer mirror inner cover
    screw inner handle
    weather strip door

## Detection Target

You can define which parts are required for presence checking.

By default, the app is configured to detect:

TARGET_CLASSES = {"weather strip door"}

This is easily modifiable in the code to check for multiple or different parts based on your use case.

## Project Structure

part_presence_checker/

├── app.py

├── detector/

│ ├── model_wrapper.py

│ ├── utils.py

│ ├── video_processor.py

│ └── init.py

├── requirements.txt

└── README.md

## Getting Started

Clone the repo

git clone https://github.com/your-username/part-presence-checker.git

cd part-presence-checker

**(Optional) Set up a virtual environment**

python -m venv venv

source venv/bin/activate (on Windows: venv\Scripts\activate)

**Install dependencies**

pip install -r requirements.txt

Run the app

streamlit run app.py

## Output

Annotated image frames saved every 3 seconds

CSV report with detection results

ZIP of all processed frames

## Model Weights

Place your YOLO model (e.g., yolo-world.pt) in the project root, or update the model path in the code.

To test with a standard model:

from ultralytics import YOLO

YOLO('yolov8n.pt').export()

## License

MIT License. Feel free to use and modify.

## Made by

Abbirami Jegan
