export interface Detection {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  confidence: number;
  severity: "Severe" | "Moderate" | "Minor";
}

export interface Counts {
  Severe: number;
  Moderate: number;
  Minor: number;
  total: number;
}

export interface PredictResponse {
  annotated_image: string; // base64 data URL
  counts: Counts;
  detections: Detection[];
  ai_explanation: string;
}
