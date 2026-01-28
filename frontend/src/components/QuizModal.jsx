import { useEffect, useState } from "react";

function QuizModal({ quizId, onClose }) {
  const [quiz, setQuiz] = useState(null);

  useEffect(() => {
    fetch(`https://wiki-quiz-app-kaoo.onrender.com/quizzes/${quizId}`)
      .then(res => res.json())
      .then(data => setQuiz(data));
  }, [quizId]);

  if (!quiz) return null;

  return (
    <>
      <div onClick={onClose} style={overlay} />

      <div style={modal}>
        <button onClick={onClose} style={closeBtn}>✖</button>

        <h2>{quiz.title}</h2>

        <pre style={quizText}>{quiz.quiz?.quiz_text}</pre>

        <h3>🔗 Related Topics</h3>
        <div style={chipContainer}>
          {quiz.related_topics.map((t, i) => (
            <span key={i} style={chip}>{t}</span>
          ))}
        </div>
      </div>
    </>
  );
}

const overlay = {
  position: "fixed",
  inset: 0,
  background: "rgba(0,0,0,0.4)",
};

const modal = {
  position: "fixed",
  top: "5%",
  left: "50%",
  transform: "translateX(-50%)",
  width: "70%",
  maxHeight: "90vh",
  overflowY: "auto",
  background: "#fff",
  padding: "25px",
  borderRadius: "10px",
  boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
};

const closeBtn = {
  float: "right",
  border: "none",
  background: "transparent",
  fontSize: "20px",
  cursor: "pointer",
};

const quizText = {
  whiteSpace: "pre-wrap",
  lineHeight: "1.6",
  marginTop: "15px",
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
};



export default QuizModal;
