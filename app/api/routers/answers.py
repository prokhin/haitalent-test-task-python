from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.post("/questions/{question_id}/answers/", response_model=schemas.Answer, status_code=201)
def create_answer_for_question(
    question_id: int,
    answer: schemas.AnswerCreate,
    db: Session = Depends(deps.get_db),
):
    """Создать ответ для указанного вопроса."""
    # Проверяем, существует ли вопрос
    db_question = crud.question.get_question(db, question_id=question_id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    return crud.answer.create_answer(db=db, answer=answer, question_id=question_id)


@router.get("/answers/{answer_id}", response_model=schemas.Answer)
def read_answer(
    answer_id: int,
    db: Session = Depends(deps.get_db),
):
    """Получить ответ по ID."""
    db_answer = crud.answer.get_answer(db, answer_id=answer_id)
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    return db_answer


@router.delete("/answers/{answer_id}", response_model=schemas.Answer)
def delete_answer(
    answer_id: int,
    db: Session = Depends(deps.get_db),
):
    """Удалить ответ по ID."""
    db_answer = crud.answer.delete_answer(db, answer_id=answer_id)
    if db_answer is None:
        raise HTTPException(status_code=404, detail="Answer not found")
    return db_answer
