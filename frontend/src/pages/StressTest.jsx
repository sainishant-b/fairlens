import { useState } from "react";
import PairComparison from "../components/PairComparison";
import BiasScore from "../components/BiasScore";
import MitigationCard from "../components/MitigationCard";
import { saveAuditResult } from "../lib/saveAudit";

const API = import.meta.env.VITE_RENDER_API_URL || "http://localhost:8000";

const DEMO_RECORD = {
  years_experience: 7,
  education_level: 3,
  num_skills: 12,
  gender_encoded: 0,
  name_origin: 0,
  zip_tier: 2,
};

export default function StressTest() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [explaining, setExplaining] = useState(false);
  const [explanation, setExplanation] = useState("");
  const [model, setModel] = useState("hiring");
  const [attribute, setAttribute] = useState("name");

  async function runTest() {
    setLoading(true);
    setError(null);
    setExplanation("");
    try {
      const res = await fetch(`${API}/stress-test`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ record: DEMO_RECORD, model, attribute }),
      });
      if (!res.ok) throw new Error(`API ${res.status}`);
      const data = await res.json();
      setResults(data);
      saveAuditResult(data.bias_report, model, attribute).catch((e) =>
        console.warn("audit save failed:", e)
      );
    } catch (e) {
      setError(e.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  async function explainBias() {
    if (!results) return;
    setExplaining(true);
    try {
      const res = await fetch(`${API}/explain-bias`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(results.bias_report),
      });
      if (!res.ok) throw new Error(`API ${res.status}`);
      const data = await res.json();
      setExplanation(data.explanation);
    } catch (e) {
      setExplanation(`(Explanation unavailable: ${e.message})`);
    } finally {
      setExplaining(false);
    }
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-bold mb-2">Adversarial Bias Stress Test</h1>
      <p className="text-gray-500 mb-6">
        Identical application. Different name. Watch the AI decide.
      </p>

      <div className="flex flex-wrap gap-3 mb-8">
        <select
          value={model}
          onChange={(e) => setModel(e.target.value)}
          className="border rounded px-3 py-2 bg-white"
        >
          <option value="hiring">Hiring Model</option>
          <option value="loan">Loan Approval Model</option>
        </select>

        <select
          value={attribute}
          onChange={(e) => setAttribute(e.target.value)}
          className="border rounded px-3 py-2 bg-white"
        >
          <option value="name">Name (ethnicity signal)</option>
          <option value="zip_code">Zip Code (income signal)</option>
        </select>

        <button
          onClick={runTest}
          disabled={loading}
          className="bg-red-600 text-white px-6 py-2 rounded font-semibold hover:bg-red-700 disabled:opacity-50"
        >
          {loading ? "Testing..." : "Run Stress Test"}
        </button>
      </div>

      {error && (
        <div className="border border-red-300 bg-red-50 text-red-800 rounded p-4 mb-6">
          {error}. Check that backend is running at {API}.
        </div>
      )}

      {results && (
        <>
          <BiasScore report={results.bias_report} />
          <PairComparison
            predictions={results.predictions}
            attribute={attribute}
          />

          <div className="mt-8">
            <button
              onClick={explainBias}
              disabled={explaining}
              className="bg-gray-900 text-white px-5 py-2 rounded text-sm hover:bg-gray-700 disabled:opacity-50"
            >
              {explaining ? "Asking Gemini..." : "Explain this bias"}
            </button>
            {explanation && (
              <div className="mt-4 border-l-4 border-gray-900 bg-white p-4 rounded">
                <p className="text-sm leading-relaxed whitespace-pre-line">
                  {explanation}
                </p>
              </div>
            )}
          </div>

          {results.mitigations && results.mitigations.length > 0 && (
            <section className="mt-10">
              <h2 className="text-lg font-semibold mb-3">Mitigation playbook</h2>
              <div className="grid md:grid-cols-2 gap-4">
                {results.mitigations.map((m, i) => (
                  <MitigationCard key={i} mitigation={m} />
                ))}
              </div>
            </section>
          )}
        </>
      )}
    </div>
  );
}
