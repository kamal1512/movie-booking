import time
import uuid

from fastapi import Request

from app.core.logger import logger


async def log_request_time(
        request: Request,
        call_next
):
    request_id = str(uuid.uuid4())

    start_time = time.perf_counter()

    response = await call_next(request)

    end_time = time.perf_counter()

    duration = (end_time - start_time) * 1000

    response.headers["X-Request-ID"] = request_id

    logger.info(
        "request_id=%s method=%s path=%s "
        "status=%s duration=%.2fms",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration
    )

    return response