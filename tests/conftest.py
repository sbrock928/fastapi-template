"""
This module contains fixtures for setting up the test environment.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.core.database import Base, engine


@pytest.fixture(autouse=True)
def test_settings():
    """Configure test settings for all tests."""
    settings.TESTING = True
    return settings


@pytest.fixture(autouse=True)
async def setup_database():
    """Create test database tables before each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)
