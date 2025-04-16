"""
Async database setup and utility functions.

This module sets up the async database connection, initializes the metadata,
and provides a dependency for async DB sessions.
"""

from typing import Annotated, AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi import Depends
import app.core.config as config

# Use in-memory SQLite for test mode
DATABASE_URL = "sqlite:///:memory:" if config.TESTING else config.SQLALCHEMY_DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind = engine, autoflush=False, expire_on_commit=False)

Base = declarative_base()

def get_session() -> Generator[Session, None, None]:
    """
    Dependency that provides an async database session with automatic cleanup.
    Ensures the session is properly closed even if an error occurs.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    """
    Initializes the database by creating all tables.
    This is meant for development/proof-of-concept only.
    """

    Base.metadata.create_all(bind=engine)



SessionDep = Annotated[Session, Depends(get_session)]