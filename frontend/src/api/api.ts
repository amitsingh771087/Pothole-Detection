import axios from "axios";
import type { PredictResponse } from "./types";

const API_BASE_URL = "http://localhost:5000";

export async function predictPotholes(file: File): Promise<PredictResponse> {
  const formData = new FormData();
  formData.append("image", file);

  const response = await axios.post<PredictResponse>(
    `${API_BASE_URL}/predict`,
    formData,
    { headers: { "Content-Type": "multipart/form-data" } }
  );

  return response.data;
}
