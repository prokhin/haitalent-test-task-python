from typing import Generator
from app.db.session import SessionLocal


def get_db() -> Generator:
    """
    Зависимость (dependency) для получения сессии базы данных.
    Гарантирует, что сессия будет закрыта после использования.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
