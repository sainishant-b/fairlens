const STYLES = {
  HIGH:   { wrap: "border-red-500 bg-red-50",     label: "text-red-700" },
  MEDIUM: { wrap: "border-yellow-500 bg-yellow-50", label: "text-yellow-700" },
  LOW:    { wrap: "border-green-500 bg-green-50", label: "text-green-700" },
};

export default function BiasScore({ report }) {
  const s = STYLES[report.bias_level] || STYLES.LOW;
  return (
    <div className={`border-2 rounded-lg p-5 mb-6 ${s.wrap}`}>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Stat label="Bias level">
          <span className={`text-4xl font-bold ${s.label}`}>
            {report.bias_level}
          </span>
        </Stat>
        <Stat label="Score disparity">
          <span className="text-4xl font-bold">
            {(report.disparity * 100).toFixed(1)}%
          </span>
        </Stat>
        <Stat label="Disadvantaged group">
          <span className="text-2xl font-semibold">
            {report.disadvantaged_group}
          </span>
        </Stat>
      </div>
    </div>
  );
}

function Stat({ label, children }) {
  return (
    <div>
      <p className="text-xs uppercase tracking-wide text-gray-500 mb-1">{label}</p>
      {children}
    </div>
  );
}
