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

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Intercepts each request and response, collects diagnostic metadata,
        and persists it to the logging database.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): A function that proceeds to the next middleware or route handler.

        Returns:
            Response: The HTTP response returned by the route handler.
        """
        # Record the start time for execution duration tracking
        start_time = time.perf_counter()

        # Read and buffer the request body
        request_body = await request.body()

        # Continue processing the request
        response = await call_next(request)

        # Calculate how long the request took
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Extract optional user ID (customize this to your auth system)
        user_id = request.headers.get("X-User-Id")

        # Extract client host, if available
        client_host = request.client.host if request.client else None

        # Build and persist a structured log entry
        log = APILog(
            method=request.method,
            path=request.url.path,
            query_string=str(request.url.query),
            request_body=request_body.decode("utf-8", errors="ignore") if request_body else None,
            response_body=getattr(response, "body", b"").decode("utf-8", errors="ignore"),
            status_code=response.status_code,
            duration_ms=duration_ms,
            user_id=user_id,
            client_host=client_host,
        )

        db = AsyncSessionLocal()
        db.add(log)
        await db.commit()
        await db.close()

        return response
