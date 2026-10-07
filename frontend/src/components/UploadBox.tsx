import { useRef, useState } from "react";

interface Props {
  onImageSelected: (file: File) => void;
  isLoading: boolean;
}

export default function UploadBox({ onImageSelected, isLoading }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleFile = (file: File | undefined) => {
    if (!file) return;
    setPreviewUrl(URL.createObjectURL(file));
    onImageSelected(file);
  };

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        Upload Road Image
      </h2>

      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          handleFile(e.dataTransfer.files?.[0]);
        }}
        className="flex flex-col items-center justify-center gap-3 border-2 border-dashed border-brand-200 rounded-xl h-64 cursor-pointer hover:bg-brand-50 transition-colors"
      >
        {previewUrl ? (
          <img
            src={previewUrl}
            alt="preview"
            className="max-h-56 rounded-lg object-contain"
          />
        ) : (
          <>
            <span className="text-4xl">📷</span>
            <p className="text-gray-500 text-sm">
              Click or drag a road photo here
            </p>
          </>
        )}
      </div>

      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={(e) => handleFile(e.target.files?.[0])}
      />

      <button
        onClick={() => inputRef.current?.click()}
        disabled={isLoading}
        className="mt-4 w-full bg-brand-600 hover:bg-brand-700 disabled:opacity-50 text-white font-medium py-2.5 rounded-xl transition-colors"
      >
        {isLoading ? "Analyzing..." : "Choose Image & Analyze"}
      </button>
    </div>
  );
}
