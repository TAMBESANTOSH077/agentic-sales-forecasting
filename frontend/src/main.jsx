import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const [region, setRegion] = useState("Pune");
  const [category, setCategory] = useState("Electronics");
  const [days, setDays] = useState(30);

  async function runForecast() {
    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();

    formData.append("region", region);
    formData.append("category", category);
    formData.append("forecast_days", days);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/forecast",
        {
          method: "POST",
          body: formData
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Forecast failed");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">

      <header className="hero">
        <span className="badge">AGENTIC AI</span>

        <h1>Sales Forecasting System</h1>

        <p>
          Multi-Agent AI system for sales prediction,
          verification and business reporting.
        </p>
      </header>

      <section className="card">

        <h2>Forecast Request</h2>

        <div className="form-grid">

          <div>
            <label>Region</label>

            <select
              value={region}
              onChange={(e) => setRegion(e.target.value)}
            >
              <option>Pune</option>
              <option>Mumbai</option>
              <option>Nashik</option>
            </select>
          </div>

          <div>
            <label>Category</label>

            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            >
              <option>Electronics</option>
              <option>Furniture</option>
            </select>
          </div>

          <div>
            <label>Forecast Days</label>

            <input
              type="number"
              min="7"
              max="90"
              value={days}
              onChange={(e) => setDays(e.target.value)}
            />
          </div>

        </div>

        <button
          onClick={runForecast}
          disabled={loading}
        >
          {loading
            ? "Running Agents..."
            : "Run Agent Workflow"}
        </button>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

      </section>

      {result && (
        <>

          <section className="card">

            <h2>Agent Activity</h2>

            {result.agent_logs.map((log, index) => (
              <div className="agent" key={index}>

                <div className={`status ${log.status}`} />

                <div>
                  <strong>{log.agent}</strong>

                  <p>{log.message}</p>
                </div>

              </div>
            ))}

          </section>

          <section className="card">

            <h2>Forecast Result</h2>

            <div className="metric">
              ₹
              {Number(
                result.forecast.total_predicted_revenue
              ).toLocaleString("en-IN")}
            </div>

            <p>
              {result.forecast.start_date}
              {" → "}
              {result.forecast.end_date}
            </p>

          </section>

          <section className="card">

            <h2>Model Validation</h2>

            <p>
              MAE:
              <strong> {result.metrics.mae}</strong>
            </p>

            <p>
              RMSE:
              <strong> {result.metrics.rmse}</strong>
            </p>

            <p>
              R²:
              <strong> {result.metrics.r2}</strong>
            </p>

            <hr />

            <h3>
              {result.forecast.verification.passed
                ? "✓ Verification Passed"
                : "⚠ Review Required"}
            </h3>

            <p>
              {result.forecast.verification.message}
            </p>

          </section>

          <section className="card">

            <h2>Executive Report</h2>

            {result.insights.map((insight, index) => (
              <div className="insight" key={index}>
                {insight}
              </div>
            ))}

          </section>

        </>
      )}

    </div>
  );
}

createRoot(
  document.getElementById("root")
).render(
  <App />
);