"""
This module sets up the TestClient for testing the FastAPI application.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
