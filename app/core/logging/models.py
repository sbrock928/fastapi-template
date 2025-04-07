"""
Database model for logging detailed API request and response interactions.

This module defines the SQLAlchemy ORM model `APILog`, which captures
comprehensive logging data for monitoring, debugging, and analytical purposes.
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime

from app.core.database import Base


class APILog(Base):
    """
    SQLAlchemy model representing logs of API requests and responses.

    This table captures detailed information for every API interaction,
    enabling comprehensive monitoring and debugging capabilities.

    Attributes:
        id (int): Primary key and unique identifier for the log entry.
        timestamp (datetime): UTC datetime when the log entry was created.
        method (str): HTTP method used in the API request (e.g., GET, POST).
        path (str): URL path requested.
        query_string (Optional[str]): URL query parameters, if any.
        request_body (Optional[str]): Raw request payload (as text).
        response_body (Optional[str]): Raw response payload (as text).
        status_code (int): HTTP status code of the API response.
        duration_ms (float): Time taken to fulfill the request, in milliseconds.
        user_id (Optional[str]): Identifier of the authenticated user, if available.
        client_host (str): IP address or hostname of the requesting client.
    """

    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    method = Column(String, nullable=False)
    path = Column(String, nullable=False)
    query_string = Column(String, nullable=True)
    request_body = Column(Text, nullable=True)
    response_body = Column(Text, nullable=True)
    status_code = Column(Integer, nullable=False)
    duration_ms = Column(Float, nullable=False)
    user_id = Column(String, nullable=True)
    client_host = Column(String, nullable=False)
