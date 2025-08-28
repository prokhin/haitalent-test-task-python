# 1. Используем официальный образ Python
FROM python:3.12-slim

# 2. Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Устанавливаем рабочую директорию
WORKDIR /app

# 4. Устанавливаем зависимости
# Сначала копируем файлы с зависимостями, чтобы кешировать этот слой
COPY pyproject.toml ./

# Устанавливаем Poetry и экспортируем зависимости в requirements.txt
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes

# Устанавливаем зависимости через pip
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем исходный код приложения
COPY . .

# 6. Открываем порт
EXPOSE 8000
