from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.models.question import Question
from app.schemas.question import QuestionCreate


def get_question(db: Session, question_id: int) -> Question | None:
    """Получить вопрос по ID вместе с ответами."""
    return db.query(Question).options(selectinload(Question.answers)).filter(Question.id == question_id).first()


def get_questions(db: Session, skip: int = 0, limit: int = 100) -> list[Question]:
    """Получить список вопросов."""
    return db.query(Question).offset(skip).limit(limit).all()


def create_question(db: Session, question: QuestionCreate) -> Question:
    """Создать новый вопрос."""
    db_question = Question(text=question.text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def delete_question(db: Session, question_id: int) -> Question | None:
    """Удалить вопрос по ID."""
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question:
        db.delete(db_question)
        db.commit()
    return db_question
