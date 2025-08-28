import datetime

from sqlalchemy import String, DateTime, text as sa_text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Question(Base):
    __tablename__ = "questions"

    # Уникальный идентификатор вопроса
    id: Mapped[int] = mapped_column(primary_key=True)
    # Текст вопроса
    text: Mapped[str] = mapped_column(String, nullable=False)
    # Дата и время создания
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=sa_text("CURRENT_TIMESTAMP")
    )

    # Связь с ответами. При удалении вопроса удаляются все связанные ответы
    answers: Mapped[list["Answer"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
        passive_deletes=True,  # Важно для ondelete="CASCADE"
    )
