import datetime
from pydantic import BaseModel, Field

from .answer import Answer


# Базовая схема для вопроса
class QuestionBase(BaseModel):
    text: str = Field(..., min_length=1, strip_whitespace=True)


# Схема для создания вопроса (используется в POST запросах)
class QuestionCreate(QuestionBase):
    pass


# Схема для чтения вопроса (используется в ответах API)
class Question(QuestionBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True


# Схема для чтения вопроса вместе с его ответами
class QuestionWithAnswers(Question):
    answers: list[Answer] = []
