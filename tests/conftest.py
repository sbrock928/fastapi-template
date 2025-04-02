"""
This module contains fixtures for setting up the test environment.
"""

import pytest
from app.core.database import Base, engine


@pytest.fixture(autouse=True)
async def reset_db() -> None:
    """
    Fixture to reset the database before each test.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
