from sqlalchemy.orm import Session

from app.models.answer import Answer
from app.schemas.answer import AnswerCreate


def get_answer(db: Session, answer_id: int) -> Answer | None:
    """Получить ответ по ID."""
    return db.query(Answer).filter(Answer.id == answer_id).first()


def create_answer(
    db: Session, answer: AnswerCreate, question_id: int
) -> Answer:
    """Создать ответ для вопроса."""
    db_answer = Answer(
        text=answer.text,
        user_id=str(answer.user_id),  # Конвертируем UUID в строку для БД
        question_id=question_id
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def delete_answer(db: Session, answer_id: int) -> Answer | None:
    """Удалить ответ по ID."""
    db_answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if db_answer:
        db.delete(db_answer)
        db.commit()
    return db_answer
