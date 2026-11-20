import os
import cv2
import pytesseract
from ultralytics import YOLO

_model = None

def get_model():
    global _model
    if _model is None:
        # The pretrained YOLOv8 nano weights are downloaded automatically on first run.
        _model = YOLO(os.getenv("YOLO_MODEL", "yolov8n.pt"))
    return _model

def detect_objects(image_path):
    model = get_model()
    results = model(image_path, verbose=False)
    labels = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            label = result.names[class_id]
            if confidence >= 0.35:
                labels.append({"label": label, "confidence": round(confidence, 2)})
    # Keep unique labels while preserving their order.
    seen, unique = set(), []
    for item in labels:
        if item["label"] not in seen:
            seen.add(item["label"])
            unique.append(item)
    return unique

def read_text(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("The uploaded image could not be read.")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    try:
        return pytesseract.image_to_string(gray).strip()
    except pytesseract.TesseractNotFoundError:
        return "OCR unavailable: install the Tesseract OCR application and ensure it is on PATH."

def describe_scene(objects):
    if not objects:
        return "I could not confidently identify objects in this image."
    names = [item["label"] for item in objects[:8]]
    return "I can see " + ", ".join(names[:-1]) + (" and " if len(names) > 1 else "") + names[-1] + "."

def analyze_image(image_path):
    objects = detect_objects(image_path)
    text = read_text(image_path)
    return {
        "objects": objects,
        "scene_description": describe_scene(objects),
        "recognized_text": text or "No readable text detected."
    }
