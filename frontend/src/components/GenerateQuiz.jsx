import { useState } from "react";

function GenerateQuiz() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generateQuiz = async () => {
    if (!url) {
      alert("Please enter a Wikipedia URL or article name");
      return;
    }

    try {
      setLoading(true);
      setResult(null);
      setError("");

      const response = await fetch(
        `http://127.0.0.1:8000/test-llm?url=${encodeURIComponent(url)}`
      );
      const data = await response.json();
      setResult(data);
    } catch {
      setError("❌ Failed to generate quiz. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={page}>
      <div style={card}>
        <h2>🔗 Generate Quiz from Wikipedia</h2>

        <input
          type="text"
          placeholder="Enter Wikipedia URL or article name (e.g. Isaac Newton)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={input}
        />

        <button onClick={generateQuiz} disabled={loading} style={button}>
          {loading ? "Generating..." : "Generate Quiz"}
        </button>

        {loading && <p style={muted}>⏳ Generating quiz using AI…</p>}
        {error && <p style={errorText}>{error}</p>}
      </div>

      {result && (
        <div style={{ ...card, marginTop: "30px" }}>
          <h2>{result.title}</h2>

          {result.quiz?.quiz_text && (
            <div style={quizBox}>
              <h3>📘 Quiz</h3>
              <pre style={quizText}>{result.quiz.quiz_text}</pre>
            </div>
          )}

          {result.related_topics && (
            <>
              <h3 style={{ marginTop: "20px" }}>🔍 Related Topics</h3>
              <div style={chipContainer}>
                {result.related_topics.map((t, i) => (
                  <span key={i} style={chip}>{t}</span>
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

/* ---------- STYLES ---------- */

const page = {
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
};

// const page = {
//   minHeight: "100vh",
//   width: "100%",
//   display: "flex",
//   justifyContent: "center",
//   alignItems: "center",
//   paddingTop: "40px",
//   boxSizing: "border-box",
// };


const card = {
  width: "100%",
  maxWidth: "850px",
  background: "#ffffff",
  padding: "25px",
  borderRadius: "12px",
  boxShadow: "0 6px 18px rgba(0,0,0,0.1)",
};

const input = {
  width: "100%",
  padding: "12px",
  marginTop: "12px",
  marginBottom: "15px",
  fontSize: "16px",
};

const button = {
  padding: "10px 20px",
  background: "#4f46e5",
  color: "#fff",
  border: "none",
  borderRadius: "8px",
  cursor: "pointer",
};

const muted = { color: "#6b7280", marginTop: "10px" };
const errorText = { color: "#dc2626" };

const quizBox = {
  background: "#f9fafb",
  padding: "15px",
  borderRadius: "8px",
  marginTop: "15px",
};

const quizText = {
  whiteSpace: "pre-wrap",
  lineHeight: "1.6",
};

const chipContainer = {
  display: "flex",
  gap: "10px",
  flexWrap: "wrap",
};

const chip = {
  background: "#e0e7ff",
  padding: "6px 12px",
  borderRadius: "20px",
  fontSize: "14px",
};

export default GenerateQuiz;
