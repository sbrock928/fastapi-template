"""
Async database setup and utility functions.

This module sets up the async database connection, initializes the metadata,
and provides a dependency for async DB sessions.
"""

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_async_session

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
