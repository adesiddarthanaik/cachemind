import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.middleware.context import request_id_context


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())

        # Store request ID in FastAPI request state
        request.state.request_id = request_id

        # Store request ID in ContextVar for global access
        request_id_context.set(request_id)

        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = (time.perf_counter() - start_time) * 1000

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.2f} ms"

        return response