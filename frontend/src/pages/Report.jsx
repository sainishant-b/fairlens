import { useEffect, useState } from "react";
import { listAuditResults } from "../lib/saveAudit";
import { isAppwriteConfigured } from "../lib/appwrite";

export default function Report() {
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!isAppwriteConfigured()) {
      setLoading(false);
      return;
    }
    listAuditResults()
      .then(setRows)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-bold mb-2">Audit History</h1>
      <p className="text-gray-500 mb-6">
        Recent stress tests run against this deployment.
      </p>

      {!isAppwriteConfigured() && (
        <div className="border border-yellow-300 bg-yellow-50 text-yellow-900 rounded p-4">
          Appwrite env vars not set. Configure VITE_APPWRITE_PROJECT_ID and
          VITE_APPWRITE_DB_ID to enable audit history.
        </div>
      )}

      {loading && <p className="text-gray-500">Loading...</p>}
      {error && <p className="text-red-600">Error: {error}</p>}

      {rows.length > 0 && (
        <div className="overflow-x-auto border rounded bg-white">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-100 text-left">
              <tr>
                <th className="px-4 py-2">Time</th>
                <th className="px-4 py-2">Model</th>
                <th className="px-4 py-2">Attribute</th>
                <th className="px-4 py-2">Bias</th>
                <th className="px-4 py-2">Disparity</th>
                <th className="px-4 py-2">Disadvantaged</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.$id} className="border-t">
                  <td className="px-4 py-2 text-gray-500">
                    {new Date(r.timestamp).toLocaleString()}
                  </td>
                  <td className="px-4 py-2">{r.model}</td>
                  <td className="px-4 py-2">{r.attribute}</td>
                  <td className="px-4 py-2 font-semibold">{r.bias_level}</td>
                  <td className="px-4 py-2">{(r.disparity * 100).toFixed(1)}%</td>
                  <td className="px-4 py-2">{r.disadvantaged_group}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
