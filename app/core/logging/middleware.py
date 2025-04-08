"""
FastAPI middleware for detailed HTTP request and response logging.

This middleware automatically captures and logs key request and response data,
including method, URL, headers, body content, status codes, processing duration,
user identity, and client IP. Logs are persisted asynchronously to a separate
SQLite database, supporting advanced debugging, performance monitoring, and
auditing use cases.

Note:
    Use this middleware in secure, trusted environments to avoid potential
    exposure of sensitive or personally identifiable information.
"""

import time
from typing import Callable, Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, StreamingResponse
from fastapi.responses import JSONResponse
from app.core.database import AsyncSessionLocal
from app.core.logging.models import APILog


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging detailed information about every incoming HTTP request
    and outgoing response handled by the FastAPI application.

    This includes:
    - HTTP method and path
    - Query string parameters
    - Request and response bodies
    - Response status code
    - Execution time in milliseconds
    - User identity (via 'X-User-Id' header)
    - Client IP address

    All logs are stored in a separate SQLite database defined in the logging module.

    Note:
        This middleware is intended for internal observability and should be used
        in trusted environments only. Avoid logging sensitive or PII data in production.
    """

    # Paths that should not be logged
    EXCLUDED_PATHS = ["/admin/logs", "/admin/logs/partial", "/openapi.json", "/docs"]

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Skip logging for excluded paths
        if any(request.url.path.startswith(path) for path in self.EXCLUDED_PATHS):
            return await call_next(request)

        start_time = time.perf_counter()

        # Read and buffer the request body once
        body_bytes = await request.body()
        # Store for later use
        request._body = body_bytes

        # Continue processing the request
        response = await call_next(request)

        # Capture response body
        response_body = None

        if isinstance(response, StreamingResponse):
            response_body = "[Streaming Response]"
        else:
            # Get the response body
            response_content = [section async for section in response.body_iterator]
            response_body = b"".join(response_content).decode("utf-8", errors="ignore")

            # Reconstruct the response with the same body
            new_response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )
            response = new_response

        # Calculate duration and create log entry
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Build and persist log entry
        log = APILog(
            method=request.method,
            path=request.url.path,
            query_string=str(request.url.query),
            request_body=body_bytes.decode("utf-8", errors="ignore") if body_bytes else None,
            response_body=response_body,
            status_code=response.status_code,
            duration_ms=duration_ms,
            user_id=request.headers.get("X-User-Id"),
            client_host=request.client.host if request.client else None,
        )

        # Save to database
        db = AsyncSessionLocal()
        try:
            db.add(log)
            await db.commit()
        finally:
            await db.close()

        return response
