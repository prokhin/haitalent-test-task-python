# 1) Базовый образ
FROM python:3.12-slim

# 2) Базовые ENV
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# 3) Системные зависимости (на случай нативных билдов)
# Если используешь psycopg[binary], можно обойтись и без build-essential,
# но оставим универсально.
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# 4) Рабочая директория
WORKDIR /app

# 5) Установка Poetry (фиксируем версию для воспроизводимости)
ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==${POETRY_VERSION}" && poetry config virtualenvs.create false

# 6) Копируем только файлы зависимостей (чтобы кеш слоёв работал)
COPY pyproject.toml poetry.lock* ./

# 7) Устанавливаем зависимости
# Для прод-образа обычно достаточно основных зависимостей:
#   --only main  (если в pyproject группы зависимостей разделены)
# Если групп нет — оставь просто `poetry install --no-root`
RUN poetry install --no-root --no-interaction --no-ansi

# 8) Копируем исходники
COPY . .

# 9) Открываем порт сервиса
EXPOSE 8000

# 10) Команда запуска:
# - сначала применяем миграции alembic
# - затем запускаем Uvicorn
# Важно: в compose укажи env_file с DATABASE_URL вида postgresql+psycopg://...@db:5432/app
CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
