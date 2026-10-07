import type { PredictResponse } from "../api/types";

interface Props {
  result: PredictResponse;
}

function CountCard({
  label,
  value,
  colorClass,
}: {
  label: string;
  value: number;
  colorClass: string;
}) {
  return (
    <div className="flex-1 bg-white rounded-xl border border-gray-200 p-4 text-center">
      <div className={`w-3 h-3 rounded-full mx-auto mb-2 ${colorClass}`} />
      <p className="text-2xl font-bold text-gray-800">{value}</p>
      <p className="text-xs text-gray-500">{label}</p>
    </div>
  );
}

export default function ResultView({ result }: Props) {
  const { annotated_image, counts, ai_explanation } = result;

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">
        Detection Result
      </h2>

      <img
        src={annotated_image}
        alt="annotated result"
        className="w-full rounded-xl border border-gray-100 mb-5"
      />

      <div className="flex gap-3 mb-5">
        <CountCard label="Severe (Red)" value={counts.Severe} colorClass="bg-severe" />
        <CountCard label="Moderate (Yellow)" value={counts.Moderate} colorClass="bg-moderate" />
        <CountCard label="Minor (Green)" value={counts.Minor} colorClass="bg-minor" />
        <CountCard label="Total Potholes" value={counts.total} colorClass="bg-brand-500" />
      </div>

      <div className="bg-brand-50 border border-brand-100 rounded-xl p-4">
        <p className="text-xs font-semibold text-brand-700 uppercase mb-1">
          AI Road Condition Summary
        </p>
        <p className="text-sm text-gray-700 leading-relaxed">{ai_explanation}</p>
      </div>
    </div>
  );
}
