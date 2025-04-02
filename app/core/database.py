"""
Async database setup and utility functions.

This module sets up the async database connection, initializes the metadata,
and provides a dependency for async DB sessions.
"""

from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from fastapi import Depends
import app.core.config as config

# Use in-memory SQLite for test mode
DATABASE_URL = "sqlite+aiosqlite:///:memory:" if config.TESTING else config.SQLALCHEMY_DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """
    Initializes the database by creating all tables.
    This is meant for development/proof-of-concept only.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
