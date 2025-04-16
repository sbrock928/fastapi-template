"""
Application setup and configuration.

This module initializes the FastAPI application, sets up the database,
includes routers, and defines custom exception handlers.
"""

from typing import AsyncGenerator
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import init_db
from app.core.router import register_routes
from app.core.logging.middleware import LoggingMiddleware





def create_app() -> FastAPI:
    app = FastAPI()
    init_db()
    app.add_middleware(LoggingMiddleware)
    register_routes(app)
    return app
