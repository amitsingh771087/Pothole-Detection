import { useState } from "react";
import UploadBox from "./components/UploadBox";
import ResultView from "./components/ResultView";
import { predictPotholes } from "./api/api";
import type { PredictResponse } from "./api/types";

export default function App() {
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelected = async (file: File) => {
    setIsLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await predictPotholes(file);
      setResult(data);
    } catch (err) {
      console.error(err);
      setError("Could not analyze image. Is the backend running on port 5000?");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <h1 className="text-xl font-bold text-gray-800">
            🛣️ Pothole Detection Dashboard
          </h1>
          <p className="text-sm text-gray-500">
            Upload a road photo to detect and classify potholes by severity
          </p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <UploadBox onImageSelected={handleImageSelected} isLoading={isLoading} />

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-xl p-4 h-fit">
              {error}
            </div>
          )}

          {result && <ResultView result={result} />}
        </div>
      </main>
    </div>
  );
}
