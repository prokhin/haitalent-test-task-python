import datetime

from sqlalchemy import ForeignKey, String, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Answer(Base):
    __tablename__ = "answers"

    # Уникальный идентификатор ответа
    id: Mapped[int] = mapped_column(primary_key=True)
    # Внешний ключ на вопрос. При удалении вопроса ответ удаляется (CASCADE)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    # Идентификатор пользователя (в формате UUID)
    user_id: Mapped[str] = mapped_column(String, nullable=False)
    # Текст ответа
    text: Mapped[str] = mapped_column(String, nullable=False)
    # Дата и время создания
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Обратная связь с вопросом
    question: Mapped["Question"] = relationship(back_populates="answers")
