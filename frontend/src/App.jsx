import { Link, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import StressTest from "./pages/StressTest";
import Report from "./pages/Report";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="border-b bg-white">
        <nav className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link to="/" className="text-xl font-bold tracking-tight">
            FairLens
          </Link>
          <div className="flex gap-6 text-sm">
            <Link to="/" className="hover:text-red-600">Home</Link>
            <Link to="/stress-test" className="hover:text-red-600">Stress Test</Link>
            <Link to="/report" className="hover:text-red-600">History</Link>
          </div>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/stress-test" element={<StressTest />} />
          <Route path="/report" element={<Report />} />
        </Routes>
      </main>
      <footer className="border-t bg-white mt-16">
        <div className="max-w-5xl mx-auto px-6 py-6 text-xs text-gray-500">
          FairLens demo. Models intentionally trained on biased data to expose hidden discrimination.
        </div>
      </footer>
    </div>
  );
}
