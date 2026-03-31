import time
import logging
from datetime import datetime
from fastapi import Request

logger = logging.getLogger("middleware")


async def logging_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = int((time.time() - start) * 1000)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"{timestamp} | {request.method} {request.url.path} | Status: {response.status_code} | Time: {duration_ms}ms"
    logger.info(msg)
    return response
