import os
from fastapi import HTTPException
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# -------------------------------------------------
# ENV
# -------------------------------------------------

print("🔥 GROQ LLM LOADED 🔥")

load_dotenv()
print("GROQ_API_KEY LOADED:", bool(os.getenv("GROQ_API_KEY")))

# -------------------------------------------------
# GROQ LLM (LLaMA 3)
# -------------------------------------------------

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0.3
)


# -------------------------------------------------
# PROMPT BUILDERS
# -------------------------------------------------

def build_quiz_prompt(content: str) -> str:
    return f"""
You are an AI that generates quizzes strictly from the provided Wikipedia content.

CONTENT:
{content}

Generate 5 quiz questions.

For each question provide:
- Question
- Four options (A, B, C, D)
- Correct answer
- Difficulty (easy / medium / hard)
- Short explanation

Return the output in clear readable text.
Do NOT include markdown.
"""

def build_related_prompt(title: str) -> str:
    return f"""
Suggest 3 related Wikipedia article titles for "{title}".
Return only the titles, one per line.
"""

# -------------------------------------------------
# LLM FUNCTIONS
# -------------------------------------------------

def generate_quiz(content: str):
    try:
        response = llm.invoke(build_quiz_prompt(content))

        print("\n========== GROQ QUIZ OUTPUT ==========\n")
        print(response.content)
        print("\n=====================================\n")

        return {
            "quiz_text": response.content
        }

    except Exception as e:
        print("GROQ QUIZ ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Failed to generate quiz")

def generate_related_topics(title: str):
    try:
        response = llm.invoke(build_related_prompt(title))

        print("\n====== GROQ RELATED TOPICS ======\n")
        print(response.content)
        print("\n================================\n")

        return [line.strip() for line in response.content.splitlines() if line.strip()]

    except Exception as e:
        print("GROQ RELATED ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Failed to generate related topics")
