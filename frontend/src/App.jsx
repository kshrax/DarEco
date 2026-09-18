import { useState } from "react";
import {
  Leaf,
  Sprout,
  Droplets,
  Mountain,
  CloudRain,
  Send,
  Loader2,
  ArrowUp,
  Clock3,
  ShieldCheck,
  BookOpen,
} from "lucide-react";

import "./App.css";

const API_URL = "https://dareco-backend.onrender.com";
const initialForm = {
  region: "Semi-arid",
  soil_organic_carbon: 0.3,
  soil_ph: 8.1,
  rainfall: "Low",
  land_use: "Monoculture wheat",
  biodiversity: "Low",
};

function App() {
  const [form, setForm] = useState(initialForm);

  const [question, setQuestion] = useState(
    "How can I improve biodiversity on my land?"
  );

  const [result, setResult] = useState(null);
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const updateField = (field, value) => {
    setForm((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const analyze = async () => {
    if (!question.trim()) {
      setError("Please enter a question first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...form,
          question: question,
          conversation_history: conversation,
        }),
      });

      if (!response.ok) {
        throw new Error("DarEco could not analyze the environment.");
      }

      const data = await response.json();

      setResult(data);

      setConversation((prev) => [
        ...prev,
        {
          role: "user",
          content: question,
        },
        {
          role: "assistant",
          content: data.recommendation || data.assessment,
        },
      ]);
    } catch (err) {
      console.error(err);

      setError(
        "Could not connect to DarEco. Make sure the FastAPI server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      {/* NAVBAR */}
      <header className="navbar">

        <div className="brand">

          <div className="brand-icon">
            <img
              src="/DarEco logo.png"
              alt="DarEco logo"
            />
          </div>

          <div>
            <h1>DarEco</h1>
            <span>Biodiversity Intelligence</span>
          </div>

        </div>

        <div className="status">
          <span className="status-dot"></span>
          AI Environmental Scientist
        </div>

      </header>

      {/* MAIN */}
      <main className="main">

        {/* HERO */}
        <section className="hero">

          <div className="hero-icon">
            <Sprout size={30} />
          </div>

          <p className="eyebrow">
            AI-POWERED ECOLOGICAL INTELLIGENCE
          </p>

          <h2>
            Understand your land.
            <br />
            <span>Improve its biodiversity.</span>
          </h2>

          <p className="hero-text">
            DarEco connects soil, climate, land use and biodiversity data to
            generate evidence-backed environmental recommendations.
          </p>

        </section>

        {/* WORKSPACE */}
        <div className="workspace">

          {/* ENVIRONMENT PROFILE */}
          <section className="card profile-card">

            <div className="card-header">

              <div>
                <p className="section-label">
                  ENVIRONMENTAL PROFILE
                </p>

                <h3>Your land</h3>
              </div>

              <Mountain size={24} />

            </div>

            <div className="fields">

              {/* REGION */}
              <div className="field">

                <label>Region</label>

                <input
                  value={form.region}
                  onChange={(e) =>
                    updateField("region", e.target.value)
                  }
                />

              </div>

              {/* SOIL */}
              <div className="field-row">

                <div className="field">

                  <label>
                    Soil organic carbon (%)
                  </label>

                  <input
                    type="number"
                    step="0.1"
                    value={form.soil_organic_carbon}
                    onChange={(e) =>
                      updateField(
                        "soil_organic_carbon",
                        Number(e.target.value)
                      )
                    }
                  />

                </div>

                <div className="field">

                  <label>Soil pH</label>

                  <input
                    type="number"
                    step="0.1"
                    value={form.soil_ph}
                    onChange={(e) =>
                      updateField(
                        "soil_ph",
                        Number(e.target.value)
                      )
                    }
                  />

                </div>

              </div>

              {/* RAINFALL */}
              <div className="field">

                <label>
                  <CloudRain size={14} />
                  Rainfall
                </label>

                <select
                  value={form.rainfall}
                  onChange={(e) =>
                    updateField(
                      "rainfall",
                      e.target.value
                    )
                  }
                >
                  <option>Low</option>
                  <option>Moderate</option>
                  <option>High</option>
                </select>

              </div>

              {/* LAND USE */}
              <div className="field">

                <label>Land use</label>

                <input
                  value={form.land_use}
                  onChange={(e) =>
                    updateField(
                      "land_use",
                      e.target.value
                    )
                  }
                />

              </div>

              {/* BIODIVERSITY */}
              <div className="field">

                <label>
                  <Leaf size={14} />
                  Biodiversity status
                </label>

                <select
                  value={form.biodiversity}
                  onChange={(e) =>
                    updateField(
                      "biodiversity",
                      e.target.value
                    )
                  }
                >
                  <option>Low</option>
                  <option>Moderate</option>
                  <option>High</option>
                  <option>Unknown</option>
                </select>

              </div>

            </div>

            {/* ANALYZE BUTTON */}
            <button
              className="analyze-btn"
              onClick={analyze}
              disabled={loading}
            >

              {loading ? (
                <>
                  <Loader2
                    size={18}
                    className="spin"
                  />
                  Analyzing...
                </>
              ) : (
                <>
                  Analyze my land
                  <ArrowUp size={18} />
                </>
              )}

            </button>

          </section>

          {/* AI PANEL */}
          <section className="right-column">

            {/* ASK DARECO */}
            <div className="card ask-card">

              <div className="card-header">

                <div>
                  <p className="section-label">
                    ASK DARECO
                  </p>

                  <h3>
                    What would you like to know?
                  </h3>
                </div>

                <Droplets size={24} />

              </div>

              <div className="question-box">

                <textarea
                  value={question}
                  onChange={(e) =>
                    setQuestion(e.target.value)
                  }
                  placeholder="Ask about biodiversity, soil, climate or land..."
                />

                <button
                  onClick={analyze}
                  disabled={loading}
                >

                  {loading ? (
                    <Loader2
                      size={19}
                      className="spin"
                    />
                  ) : (
                    <Send size={19} />
                  )}

                </button>

              </div>

            </div>

            {/* ERROR */}
            {error && (
              <div className="error">
                {error}
              </div>
            )}

            {/* CONVERSATION */}
            {conversation.length > 0 && (
              <div className="card conversation-card">

                <div className="card-header">

                  <div>

                    <p className="section-label">
                      CONVERSATION
                    </p>

                    <h3>DarEco context</h3>

                  </div>

                  <Leaf size={22} />

                </div>

                <div className="conversation-list">

                  {conversation.map(
                    (message, index) => (

                      <div
                        key={index}
                        className={`conversation-message ${
                          message.role === "user"
                            ? "user-message"
                            : "assistant-message"
                        }`}
                      >

                        <div className="message-label">
                          {message.role === "user"
                            ? "You"
                            : "DarEco"}
                        </div>

                        <p>
                          {message.content}
                        </p>

                      </div>

                    )
                  )}

                </div>

              </div>
            )}

            {/* EMPTY STATE */}
            {!result && !loading && (
              <div className="card empty-state">

                <div className="empty-icon">
                  <Leaf size={28} />
                </div>

                <h3>
                  Your ecological assessment will appear here
                </h3>

                <p>
                  Enter your environmental conditions and let
                  DarEco reason across multiple ecological variables.
                </p>

              </div>
            )}

            {/* LOADING */}
            {loading && (
              <div className="card loading-state">

                <Loader2
                  size={32}
                  className="spin"
                />

                <h3>
                  Analyzing your ecosystem...
                </h3>

                <p>
                  Retrieving environmental knowledge and connecting
                  multiple variables.
                </p>

              </div>
            )}

            {/* RESULTS */}
            {result && !loading && (
              <Result result={result} />
            )}

          </section>

        </div>

      </main>

      {/* FOOTER */}
      <footer>

        <Leaf size={15} />

        DarEco · Evidence-backed biodiversity intelligence

      </footer>

    </div>
  );
}


/* =========================================================
   RESULT COMPONENT
========================================================= */

function Result({ result }) {

  return (

    <div className="results">

      {/* ASSESSMENT */}
      <div className="card assessment-card">

        <div className="result-title">

          <div className="result-icon">
            <Sprout size={22} />
          </div>

          <div>

            <p className="section-label">
              ASSESSMENT
            </p>

            <h3>
              Ecological assessment
            </h3>

          </div>

        </div>

        <p className="assessment-text">
          {result.assessment}
        </p>

      </div>


      {/* RECOMMENDATION */}
      <div className="card recommendation-card">

        <div className="recommendation-heading">

          <span>🌱</span>

          <div>

            <p className="section-label">
              RECOMMENDATION
            </p>

            <h3>
              What to do
            </h3>

          </div>

        </div>

        <p className="recommendation">
          {result.recommendation}
        </p>

      </div>


      {/* REASONING */}
      <div className="card">

        <div className="card-header">

          <div>

            <p className="section-label">
              SCIENTIFIC REASONING
            </p>

            <h3>
              Why it works
            </h3>

          </div>

          <BookOpen size={22} />

        </div>

        <p className="reasoning">
          {result.reasoning}
        </p>

      </div>


      {/* METRICS */}
      <div className="metric-grid">

        <div className="card">

          <div className="mini-heading">

            <ArrowUp size={18} />

            <span>
              Impacted metrics
            </span>

          </div>

          <div className="metrics">

            {result.impacted_metrics?.map(
              (metric, index) => (

                <span
                  key={index}
                  className="metric"
                >

                  {metric}

                  <ArrowUp size={13} />

                </span>

              )
            )}

          </div>

        </div>


        <div className="card">

          <div className="mini-heading">

            <Clock3 size={18} />

            <span>
              Time horizon
            </span>

          </div>

          <p className="big-value">
            {result.time_horizon}
          </p>

        </div>


        <div className="card">

          <div className="mini-heading">

            <ShieldCheck size={18} />

            <span>
              Confidence
            </span>

          </div>

          <p className="big-value">
            {result.confidence}
          </p>

        </div>

      </div>


      {/* EVIDENCE */}
      <div className="card evidence-card">

        <div className="card-header">

          <div>

            <p className="section-label">
              KNOWLEDGE RETRIEVAL
            </p>

            <h3>
              Evidence used
            </h3>

          </div>

          <BookOpen size={22} />

        </div>


        <div className="evidence-list">

          {result.evidence?.map(
            (item, index) => (

              <div
                className="evidence-item"
                key={index}
              >

                <div className="evidence-number">
                  {index + 1}
                </div>

                <div className="evidence-content">

                  <strong>
                    {item.topic}
                  </strong>

                  <p>
                    {item.source}
                  </p>

                </div>

                <span className="evidence-badge">
                  Retrieved
                </span>

              </div>

            )
          )}

        </div>

      </div>

    </div>
  );
}

export default App;