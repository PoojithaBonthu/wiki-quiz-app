from sqlalchemy import Column, Integer, String, Text, JSON
from .database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text)
    quiz_data = Column(JSON)
    related_topics = Column(JSON)
