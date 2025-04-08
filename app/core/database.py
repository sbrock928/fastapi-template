"""
Async database setup and utility functions.

This module sets up the async database connection, initializes the metadata,
and provides a dependency for async DB sessions.
"""

from typing import Annotated, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from fastapi import Depends
from app.core.config import settings

# Use in-memory SQLite for test mode
DATABASE_URL = "sqlite+aiosqlite:///:memory:" if settings.TESTING else settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an async database session with automatic cleanup.
    Ensures the session is properly closed even if an error occurs.
    """
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()


async def init_db() -> None:
    """
    Initializes the database by creating all tables.
    This is meant for development/proof-of-concept only.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
