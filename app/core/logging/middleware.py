"""
This module contains middleware for logging detailed HTTP request and response data into a database.
"""

import getpass
import socket
import time
from typing import Callable, Awaitable, List, Dict, Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from starlette.types import Message

from app.core.database import SessionLocal
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
    EXCLUDED_PATHS = ["/logs", "/openapi.json", "/docs"]

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Skip logging for excluded paths
        if any(request.url.path.startswith(path) for path in self.EXCLUDED_PATHS):
            return await call_next(request)

        start_time = time.perf_counter()

        # Read and buffer the request body once
        body_bytes = await request.body()

        # Continue processing the request
        response = await call_next(request)

        # Capture response body
        response_body = None

        if isinstance(response, StreamingResponse):
            response_body = "[Streaming Response]"
        else:
            # Get the response body using the raw response interface
            response_content: List[bytes] = []

            # Create a custom receive function that returns the response chunks
            async def receive() -> Message:
                return {"type": "http.response.body", "body": b"", "more_body": False}

            # Create a custom send function that captures the response body
            async def send(message: Message) -> None:
                if message["type"] == "http.response.body":
                    if "body" in message:
                        response_content.append(message["body"])

            # Create proper ASGI scope
            scope: Dict[str, Any] = {
                "type": "http",
                "asgi": {"version": "3.0"},
                "http_version": "1.1",
            }

            # Call the response with proper scope
            await response(scope, receive, send)

            response_body = b"".join(response_content).decode("utf-8", errors="ignore")

            # Reconstruct the response with the same body
            new_response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )
            response = new_response

        duration_ms = (time.perf_counter() - start_time) * 1000
        user_id = getpass.getuser()
        client_host = socket.gethostname()

        # Build and persist log entry
        log_entry = APILog(
            method=request.method,
            path=request.url.path,
            query_string=str(request.url.query),
            request_body=body_bytes.decode("utf-8", errors="ignore") if body_bytes else None,
            response_body=response_body,
            status_code=response.status_code,
            duration_ms=duration_ms,
            user_id=user_id,
            client_host=client_host,
        )

        with SessionLocal() as db:
            db.add(log_entry)
            db.commit()

        return response
