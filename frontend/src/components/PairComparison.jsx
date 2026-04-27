export default function PairComparison({ predictions, attribute }) {
  return (
    <div>
      <h2 className="text-lg font-semibold mb-3">
        Same qualifications. Different outcomes.
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {predictions.map((p, i) => {
          const approved = p.score > 0.5;
          const headline =
            attribute === "zip_code" ? `Zip ${p.zip_code}` : p.name || p._group;
          return (
            <div
              key={i}
              className={`rounded-lg border p-4 bg-white ${
                approved
                  ? "border-green-400"
                  : "border-red-400"
              }`}
            >
              <p className="font-bold text-lg">{headline}</p>
              <p className="text-xs text-gray-500 mb-3">Group: {p._group}</p>
              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div
                  className={`h-3 ${approved ? "bg-green-500" : "bg-red-500"}`}
                  style={{ width: `${Math.max(p.score * 100, 2)}%` }}
                />
              </div>
              <p className="mt-2 text-sm flex justify-between">
                <span className="text-gray-600">
                  {(p.score * 100).toFixed(1)}%
                </span>
                <span
                  className={`font-semibold ${
                    approved ? "text-green-700" : "text-red-700"
                  }`}
                >
                  {approved ? "APPROVED" : "REJECTED"}
                </span>
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
