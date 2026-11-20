# VisionGuide AI

An educational assistive-technology prototype that combines object detection, OCR, and browser-based speech output to describe an uploaded or camera-captured image.

## Features

- Object detection using the Ultralytics YOLO model.
- Text extraction from images using Tesseract OCR.
- Basic scene summary generated from detected objects.
- Text-to-speech using the browser Speech Synthesis API.
- Flask web interface that supports image upload and mobile camera capture.

## Requirements

- Python 3.10 or newer.
- Tesseract OCR installed separately on your computer.
- Internet access on first run so Ultralytics can download the YOLO model weights.

## Setup

### 1. Create and activate a virtual environment

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**
```powershell
py -m venv .venv
.venv\Scripts\activate
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

- macOS (Homebrew): `brew install tesseract`
- Ubuntu/Debian: `sudo apt install tesseract-ocr`
- Windows: Install Tesseract OCR and add its installation directory to PATH.

Verify installation:
```bash
tesseract --version
```

### 4. Run the application

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser. Select an image or use the camera capture option, then choose **Analyze image**.

## GitHub upload

Do not commit model weights, virtual environments, `.env` files, or private data. The `.gitignore` file excludes these by default.

## Important limitations and safety

This is a prototype for learning and demonstration. It analyzes a still image, not continuous live video. Its scene description is a simple summary of detected object labels, not a full visual-language model interpretation. OCR quality depends on image clarity and language configuration. Object detection can miss objects or produce incorrect labels.

**Never rely on this prototype for obstacle avoidance, road crossing, navigation, or emergency decisions.** It is not a substitute for a white cane, guide dog, or trained assistance.
