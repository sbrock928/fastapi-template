"""
Database model for logging detailed API request and response interactions.

This module defines the SQLAlchemy ORM model `APILog`, which captures
comprehensive logging data for monitoring, debugging, and analytical purposes.
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
import pytz
from typing import Optional

from app.core.database import Base


class APILog(Base):
    """
    SQLAlchemy model representing logs of API requests and responses.

    This table captures detailed information for every API interaction,
    enabling comprehensive monitoring and debugging capabilities.

    Attributes:
        id (Mapped[int]): Primary key and unique identifier for the log entry.
        created_at (Mapped[datetime]): Eastern timezone datetime when the log entry was created.
        method (Mapped[str]): HTTP method used in the API request (e.g., GET, POST).
        path (Mapped[str]): URL path requested.
        query_string (Mapped[str]): URL query parameters as a string.
        request_body (Mapped[Optional[str]]): Raw request payload (as text), if any.
        response_body (Mapped[Optional[str]]): Raw response payload (as text), if any.
        status_code (Mapped[int]): HTTP status code of the API response.
        duration_ms (Mapped[float]): Time taken to fulfill the request, in milliseconds.
        user_id (Mapped[Optional[str]]): Identifier of the authenticated user, if available.
        client_host (Mapped[Optional[str]]): IP address or hostname of the requesting client.

    Note:
        - All timestamps are stored in Eastern Time (America/New_York)
        - Query strings are stored as raw strings, not parsed parameters
        - Request and response bodies may be truncated for large payloads
    """

    __tablename__ = "api_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(
            pytz.timezone("America/New_York")
        ),  # Set default to Eastern timezone
    )
    method: Mapped[str]
    path: Mapped[str]
    query_string: Mapped[str]
    request_body: Mapped[Optional[str]]
    response_body: Mapped[Optional[str]]
    status_code: Mapped[int]
    duration_ms: Mapped[float]
    user_id: Mapped[Optional[str]]
    client_host: Mapped[Optional[str]]
