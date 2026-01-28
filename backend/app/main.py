from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, SessionLocal
from .models import Base, Quiz
from .scraper import scrape_wikipedia
from .llm import generate_quiz, generate_related_topics

app = FastAPI(
    title="Wiki Quiz Generator API",
    description="Generate quizzes from Wikipedia articles using LLM",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables (safe if already exists)
Base.metadata.create_all(bind=engine)

# -----------------------------
# Database Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def root():
    return {"message": "Wiki Quiz API is running"}

@app.get("/test-scrape")
def test_scrape(url: str):
    return scrape_wikipedia(url)

# -----------------------------
# Generate Quiz + Store in DB
# -----------------------------
@app.get("/test-llm")
def test_llm(url: str, db: Session = Depends(get_db)):
    data = scrape_wikipedia(url)

    # Check if quiz already exists
    existing_quiz = db.query(Quiz).filter(Quiz.url == url).first()
    if existing_quiz:
        return {
            "message": "Quiz already exists",
            "quiz_id": existing_quiz.id,
            "title": existing_quiz.title
        }

    quiz = generate_quiz(data["content"])
    related = generate_related_topics(data["title"])

    new_quiz = Quiz(
        url=url,
        title=data["title"],
        summary=data["summary"],
        quiz_data=quiz,
        related_topics=related
    )

    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    return {
        "id": new_quiz.id,
        "title": new_quiz.title,
        "quiz": quiz,
        "related_topics": related
    }

# -----------------------------
# TAB 2 – Past Quizzes (History)
# -----------------------------
@app.get("/quizzes")
def get_all_quizzes(db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).all()
    return [
        {
            "id": q.id,
            "url": q.url,
            "title": q.title
        }
        for q in quizzes
    ]

# -----------------------------
# Quiz Details (Modal)
# -----------------------------
@app.get("/quizzes/{quiz_id}")
def get_quiz_by_id(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()

    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return {
        "id": quiz.id,
        "url": quiz.url,
        "title": quiz.title,
        "summary": quiz.summary,
        "quiz": quiz.quiz_data,
        "related_topics": quiz.related_topics
    }
