"""
This module contains fixtures for setting up the test environment.
"""

import pytest
from app.core.database import Base, engine


@pytest.fixture(autouse=True)
def reset_db() -> None:
    """
    Fixture to reset the database before each test.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
