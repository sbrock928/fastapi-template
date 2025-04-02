"""
Database setup and utility functions.

This module sets up the database connection, initializes the database,
and provides a generator for database sessions.
"""

from typing import Annotated, Iterator

import app.core.config as config
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:" if config.TESTING else config.SQLALCHEMY_DATABASE_URL

engine = create_engine(config.SQLALCHEMY_DATABASE_URL)

Base = declarative_base()


def init_db() -> None:
    """
    Initializes the database by creating all tables.
    """
    Base.metadata.create_all(bind=engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
