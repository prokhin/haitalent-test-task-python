import datetime
import uuid

from pydantic import BaseModel, Field


# Базовая схема для ответа
class AnswerBase(BaseModel):
    text: str = Field(..., min_length=1, strip_whitespace=True)


# Схема для создания ответа
class AnswerCreate(AnswerBase):
    user_id: uuid.UUID  # Валидация UUID v4


# Схема для чтения ответа
class Answer(AnswerBase):
    id: int
    question_id: int
    user_id: uuid.UUID
    created_at: datetime.datetime

    class Config:
        from_attributes = True
