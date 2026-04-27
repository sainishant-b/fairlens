const EFFORT_COLOR = {
  low: "bg-green-100 text-green-800",
  medium: "bg-yellow-100 text-yellow-800",
  high: "bg-red-100 text-red-800",
};

export default function MitigationCard({ mitigation }) {
  const effortClass = EFFORT_COLOR[mitigation.effort] || "bg-gray-100 text-gray-800";
  return (
    <div className="border rounded-lg bg-white p-4">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-semibold">{mitigation.name}</h3>
        <span className={`text-xs px-2 py-0.5 rounded ${effortClass}`}>
          {mitigation.effort} effort
        </span>
      </div>
      <p className="text-sm text-gray-700 mb-3">{mitigation.summary}</p>
      <p className="text-xs text-gray-500">
        Expected disparity reduction:{" "}
        <span className="font-semibold text-gray-800">
          {mitigation.expected_disparity_reduction}
        </span>
      </p>
    </div>
  );
}
