import { useState } from "react";
import GenerateQuiz from "./components/GenerateQuiz";
import History from "./components/History";

function App() {
  const [activeTab, setActiveTab] = useState("generate");

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Wiki Quiz Generator</h1>

      <div style={{ marginBottom: "20px" }}>
        <button onClick={() => setActiveTab("generate")}>
          Generate Quiz
        </button>
        <button onClick={() => setActiveTab("history")} style={{ marginLeft: "10px" }}>
          Past Quizzes
        </button>
      </div>

      {activeTab === "generate" && <GenerateQuiz />}
      {activeTab === "history" && <History />}
    </div>
  );
}

export default App;
