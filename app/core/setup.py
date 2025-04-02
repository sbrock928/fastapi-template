"""
Application setup and configuration.

This module initializes the FastAPI application, sets up the database,
includes routers, and defines custom exception handlers.
"""

from fastapi import FastAPI
from app.core.db import init_db

def create_app() -> FastAPI:
    app = FastAPI()
    init_db()

    return app
