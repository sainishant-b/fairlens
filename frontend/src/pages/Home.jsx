import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="max-w-4xl mx-auto px-6 py-16">
      <h1 className="text-5xl font-bold tracking-tight mb-4">
        Same resume. Different name. Different fate.
      </h1>
      <p className="text-lg text-gray-600 mb-8 max-w-2xl">
        FairLens stress tests AI hiring and lending models with adversarial inputs that
        expose hidden discrimination - bias an average fairness audit would miss.
      </p>

      <Link
        to="/stress-test"
        className="inline-block bg-red-600 text-white px-8 py-3 rounded font-semibold hover:bg-red-700"
      >
        Run a Stress Test
      </Link>

      <section className="mt-16 grid md:grid-cols-3 gap-6">
        <Card title="1. Pick a model">
          Hiring or loan approval. Both pre-trained on intentionally biased
          historical data.
        </Card>
        <Card title="2. Pick an attribute">
          Name (ethnicity signal) or zip code (income signal). FairLens generates
          identical records that differ only in that attribute.
        </Card>
        <Card title="3. See the bias">
          Side-by-side scores. Disparity meter. Mitigation playbook.
          Plain-English explanation from Gemini.
        </Card>
      </section>
    </div>
  );
}

function Card({ title, children }) {
  return (
    <div className="border rounded-lg bg-white p-5">
      <h3 className="font-semibold mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{children}</p>
    </div>
  );
}
