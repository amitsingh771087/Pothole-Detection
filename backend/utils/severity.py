"""
severity.py
------------
Decides how "bad" each detected pothole is and which color it should be
drawn in on the output image.

Rule used (simple, explainable, good for an MSc report):
    severity_score = (box_area / image_area) * confidence

    score >= SEVERE_THRESHOLD    -> "Severe"   -> RED
    score >= MODERATE_THRESHOLD  -> "Moderate" -> YELLOW
    otherwise                    -> "Minor"    -> GREEN

The idea: a pothole that is both LARGE (relative to the frame) and
detected with HIGH confidence is more likely to be a real, dangerous
pothole -> classified as Severe. Small / low-confidence detections are
treated as Minor cracks/potholes.

You can tune the two thresholds below once you train on your own
dataset and look at the real box-size distribution.
"""

from dataclasses import dataclass

SEVERE_THRESHOLD = 0.06     # >= 6% of the frame area (weighted by confidence)
MODERATE_THRESHOLD = 0.02   # >= 2% of the frame area

# BGR colors (OpenCV uses BGR, not RGB)
COLOR_SEVERE = (0, 0, 255)      # Red
COLOR_MODERATE = (0, 255, 255)  # Yellow
COLOR_MINOR = (0, 200, 0)       # Green


@dataclass
class Detection:
    x1: int
    y1: int
    x2: int
    y2: int
    confidence: float
    severity: str
    color: tuple


def classify_severity(box, confidence: float, image_shape) -> Detection:
    """
    box: (x1, y1, x2, y2) in pixel coordinates
    confidence: model confidence for this box (0-1)
    image_shape: (height, width, channels) of the original image
    """
    x1, y1, x2, y2 = box
    img_h, img_w = image_shape[0], image_shape[1]

    box_area = max(0, (x2 - x1)) * max(0, (y2 - y1))
    image_area = img_h * img_w
    relative_area = box_area / image_area if image_area > 0 else 0

    score = relative_area * confidence

    if score >= SEVERE_THRESHOLD:
        severity, color = "Severe", COLOR_SEVERE
    elif score >= MODERATE_THRESHOLD:
        severity, color = "Moderate", COLOR_MODERATE
    else:
        severity, color = "Minor", COLOR_MINOR

    return Detection(x1, y1, x2, y2, confidence, severity, color)


def summarize(detections):
    """Returns counts per severity + total, used by the API response."""
    summary = {"Severe": 0, "Moderate": 0, "Minor": 0}
    for d in detections:
        summary[d.severity] += 1
    summary["total"] = len(detections)
    return summary
