from fastapi import FastAPI

from app.api.routers import questions, answers
from app.core.logging import logging_middleware

# Создаем экземпляр приложения FastAPI
app = FastAPI(
    title="Q&A Service",
    description="API для сервиса вопросов и ответов",
    version="0.1.0",
)

# Подключаем middleware для логирования
app.middleware("http")(logging_middleware)

# Подключаем роутеры
app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(answers.router, tags=["Answers"]) # префикс уже в роутере


@app.get("/", tags=["Root"])
def read_root():
    """Корневой эндпоинт для проверки доступности сервиса."""
    return {"message": "Welcome to Q&A API"}
