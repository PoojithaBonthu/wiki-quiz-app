import { useEffect, useState } from "react";
import QuizModal from "./QuizModal";

function History() {
  const [quizzes, setQuizzes] = useState([]);
  const [selectedQuiz, setSelectedQuiz] = useState(null);

  useEffect(() => {
    fetch("https://wiki-quiz-app-kaoo.onrender.com/quizzes")
      .then(res => res.json())
      .then(data => setQuizzes(data));
  }, []);

  return (
    <div style={page}>
      <div style={card}>
        <h2>📚 Past Quizzes</h2>

        <table style={table}>
          <thead>
            <tr>
              <th style={th}>ID</th>
              <th style={th}>Title</th>
              <th style={th}>Action</th>
            </tr>
          </thead>
          <tbody>
            {quizzes.map(q => (
              <tr key={q.id}>
                <td style={tdCenter}>{q.id}</td>
                <td style={tdLeft}>{q.title}</td>
                <td style={tdCenter}>
                  <button style={button} onClick={() => setSelectedQuiz(q.id)}>
                    View Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedQuiz && (
        <QuizModal
          quizId={selectedQuiz}
          onClose={() => setSelectedQuiz(null)}
        />
      )}
    </div>
  );
}

/* ---------- STYLES ---------- */

const page = {
  display: "flex",
  justifyContent: "center",
};

const card = {
  width: "100%",
  maxWidth: "700px",
  background: "#fff",
  padding: "25px",
  borderRadius: "12px",
  boxShadow: "0 6px 18px rgba(0,0,0,0.1)",
};

const table = {
  width: "100%",
  borderCollapse: "collapse",
  marginTop: "15px",
};

const th = {
  textAlign: "center",
  padding: "10px",
  borderBottom: "2px solid #e5e7eb",
};

const tdCenter = {
  textAlign: "center",
  padding: "10px",
  borderBottom: "1px solid #e5e7eb",
};

const tdLeft = {
  textAlign: "left",
  padding: "10px",
  borderBottom: "1px solid #e5e7eb",
};

const button = {
  padding: "6px 14px",
  background: "#4f46e5",
  color: "#fff",
  border: "none",
  borderRadius: "6px",
};

export default History;
