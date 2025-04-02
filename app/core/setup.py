"""
Application setup and configuration.

This module initializes the FastAPI application, sets up the database,
includes routers, and defines custom exception handlers.
"""

from fastapi import FastAPI

from app.core.database import init_db
from app.core.router import register_routes


def create_app() -> FastAPI:
    app = FastAPI()
    init_db()
    register_routes(app)

    return app
