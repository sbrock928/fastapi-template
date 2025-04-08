"""
This module contains fixtures for setting up the test environment.
"""

from typing import AsyncGenerator
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings, Settings
from app.core.database import Base, engine

# This needs to run before any database operations
settings.TESTING = True


@pytest.fixture(scope="session", autouse=True)
def test_settings() -> Settings:
    """Configure test settings for all tests."""
    return settings


@pytest.fixture(autouse=True)
async def setup_database() -> AsyncGenerator[None, None]:
    """Create test database tables before each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI application."""
    return TestClient(app)
