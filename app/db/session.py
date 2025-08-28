from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Создаем "движок" для подключения к БД
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Создаем класс для сессий SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
