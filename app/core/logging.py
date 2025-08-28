import logging
import time

from fastapi import Request, Response
from pythonjsonlogger import jsonlogger

# Создаем логгер
logger = logging.getLogger("qa_api_logger")
logger.setLevel(logging.INFO)

# Создаем обработчик для вывода в консоль
logHandler = logging.StreamHandler()

# Создаем JSON-форматтер
formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
)

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


async def logging_middleware(request: Request, call_next) -> Response:
    """
    Middleware для логирования HTTP-запросов и ответов.
    Логирует метод, URL, код ответа и время выполнения.
    """
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000  # в миллисекундах

    logger.info(
        "Request processed",
        extra={
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "process_time_ms": round(process_time, 2),
        },
    )

    return response
