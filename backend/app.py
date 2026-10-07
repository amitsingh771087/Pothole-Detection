"""
app.py
------
Flask API for the Pothole Detection Dashboard.

Endpoints:
    GET  /health          -> simple health check
    POST /predict          -> upload an image, get back:
        {
            "annotated_image": "data:image/jpeg;base64,....",
            "counts": {"Severe": 2, "Moderate": 1, "Minor": 0, "total": 3},
            "detections": [ {x1,y1,x2,y2,confidence,severity}, ... ],
            "ai_explanation": "..."
        }

Run:
    pip install -r requirements.txt
    python app.py
    -> server starts on http://localhost:5000
"""

import base64
import io

import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from ultralytics import YOLO

from utils.severity import classify_severity, summarize
from utils.ai_explain import generate_ai_explanation

app = Flask(__name__)
CORS(app)  # allow the React dev server (localhost:5173) to call this API

# ---------------------------------------------------------------------------
# Load the trained model once at startup.
#
# For a quick start / class demo you can use a generic YOLOv8 checkpoint,
# but for real pothole detection you MUST train on a pothole dataset
# (see model/train_model.py for the training script + dataset link).
#
# Put your trained weights file here after training:
#   backend/model/pothole_best.pt
# ---------------------------------------------------------------------------
MODEL_PATH = "model/pothole_best.pt"
CONF_THRESHOLD = 0.25

try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"[WARN] Could not load {MODEL_PATH}: {e}")
    print("[WARN] Falling back to the base yolov8n model (not pothole-trained).")
    model = YOLO("yolov8n.pt")


def read_image_from_request(file_storage) -> np.ndarray:
    image = Image.open(file_storage.stream).convert("RGB")
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def encode_image_to_base64(image_bgr: np.ndarray) -> str:
    success, buffer = cv2.imencode(".jpg", image_bgr)
    if not success:
        raise RuntimeError("Could not encode output image")
    b64 = base64.b64encode(buffer).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided (field name: 'image')"}), 400

    file = request.files["image"]
    image_bgr = read_image_from_request(file)

    results = model.predict(source=image_bgr, conf=CONF_THRESHOLD, verbose=False)
    result = results[0]

    detections = []
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        confidence = float(box.conf[0])
        det = classify_severity((x1, y1, x2, y2), confidence, image_bgr.shape)
        detections.append(det)

    # Draw boxes + labels on a copy of the original image
    annotated = image_bgr.copy()
    for d in detections:
        cv2.rectangle(annotated, (d.x1, d.y1), (d.x2, d.y2), d.color, 3)
        label = f"{d.severity} {d.confidence:.2f}"
        cv2.putText(annotated, label, (d.x1, max(0, d.y1 - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, d.color, 2)

    counts = summarize(detections)
    ai_explanation = generate_ai_explanation(counts)

    response = {
        "annotated_image": encode_image_to_base64(annotated),
        "counts": counts,
        "detections": [
            {
                "x1": d.x1, "y1": d.y1, "x2": d.x2, "y2": d.y2,
                "confidence": round(d.confidence, 3),
                "severity": d.severity,
            }
            for d in detections
        ],
        "ai_explanation": ai_explanation,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
