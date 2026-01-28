from pydantic import BaseModel
from typing import List, Dict, Any

class QuizBase(BaseModel):
    url: str
    title: str
    summary: str
    quiz_data: Any
    related_topics: Any

class QuizResponse(QuizBase):
    id: int

    class Config:
        orm_mode = True
