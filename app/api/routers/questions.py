from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Question])
def read_questions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """Получить список вопросов."""
    questions = crud.question.get_questions(db, skip=skip, limit=limit)
    return questions


@router.post("/", response_model=schemas.Question, status_code=201)
def create_question(
    question: schemas.QuestionCreate,
    db: Session = Depends(deps.get_db),
):
    """Создать новый вопрос."""
    return crud.question.create_question(db=db, question=question)


@router.get("/{question_id}", response_model=schemas.QuestionWithAnswers)
def read_question(
    question_id: int,
    db: Session = Depends(deps.get_db),
):
    """Получить вопрос по ID вместе со всеми ответами."""
    db_question = crud.question.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@router.delete("/{question_id}", response_model=schemas.Question)
def delete_question(
    question_id: int,
    db: Session = Depends(deps.get_db),
):
    """Удалить вопрос (и все связанные с ним ответы)."""
    db_question = crud.question.delete_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question
