# Pothole Detection Dashboard

A simple end-to-end Data Science project: upload a real-world road photo,
detect potholes with a trained YOLOv8 model, classify each pothole's
severity (Red = Severe, Yellow = Moderate, Green = Minor), count them,
and show an AI-generated road condition summary — all in a React
dashboard.

## File Structure

```
pothole-detection/
├── backend/
│   ├── app.py                  # Flask API (/predict endpoint)
│   ├── requirements.txt
│   ├── model/
│   │   ├── train_model.py      # Script to train YOLOv8 on pothole dataset
│   │   └── pothole_best.pt     # <- your trained weights go here
│   └── utils/
│       ├── severity.py         # Red/Yellow/Green severity classification
│       └── ai_explain.py       # AI-generated road condition explanation
│
└── frontend/                   # React + TypeScript + Tailwind CSS
    ├── index.html
    ├── package.json
    ├── tailwind.config.js
    └── src/
        ├── App.tsx
        ├── main.tsx
        ├── index.css
        ├── api/
        │   ├── api.ts           # calls the Flask backend
        │   └── types.ts
        └── components/
            ├── UploadBox.tsx    # image upload UI
            └── ResultView.tsx   # annotated image + counts + AI summary
```

## How it works (pipeline)

1. **User uploads an image** in the React dashboard.
2. The image is sent to the Flask backend (`POST /predict`).
3. **YOLOv8** (trained on a pothole dataset) detects potholes and returns
   bounding boxes + confidence scores.
4. `severity.py` scores each box using:
   `severity_score = (box_area / image_area) * confidence`
   - Large + confident detections → **Severe (Red)**
   - Medium → **Moderate (Yellow)**
   - Small/low-confidence → **Minor (Green)**
5. The image is annotated with colored boxes and sent back as base64.
6. `ai_explain.py` turns the counts into a short natural-language report
   (rule-based by default; can call the Claude API if `ANTHROPIC_API_KEY`
   is set, for a richer explanation).
7. The dashboard displays the annotated image, per-severity counts, and
   the AI summary.

## Setup

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Train the model** (or download a pretrained pothole checkpoint):

```bash
cd model
# 1. Download a pothole dataset in YOLOv8 format (Roboflow Universe or
#    Kaggle "Pothole Detection Dataset") into model/dataset/
# 2. Train:
python train_model.py
# 3. Copy runs/detect/pothole_train/weights/best.pt -> model/pothole_best.pt
```

**Run the API:**

```bash
cd backend
python app.py
# -> http://localhost:5000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
# -> http://localhost:5173
```

Open the dashboard, upload a road photo, and view the results.

## Tech Stack

| Layer            | Tool                                  |
|-------------------|----------------------------------------|
| Object Detection   | YOLOv8 (Ultralytics), OpenCV, Pillow  |
| Backend API        | Python, Flask, Flask-CORS             |
| Frontend           | React, TypeScript, Vite, Tailwind CSS |
| AI Explanation     | Rule-based summary (optional Claude API) |

## Notes for the report

- **Dataset**: Kaggle / Roboflow public pothole image datasets (annotated
  with bounding boxes) — cite the exact dataset you use.
- **Model**: YOLOv8n (nano) fine-tuned via transfer learning — small and
  fast enough to train on a laptop/Colab, good for a semester project.
- **Severity logic** is a simple, explainable heuristic (box size ×
  confidence) — you can extend it later with pothole depth estimation.
- The light Tailwind theme uses a blue "brand" accent with red / yellow /
  green severity indicators to keep the UI clean for a dashboard demo.
