"""
Module for registering routes in the FastAPI application.
"""

from fastapi import FastAPI

from app.users.routes import router as user_router
from app.core.logging.routes import router as logging_router


def register_routes(app: FastAPI) -> None:
    """
    Registers all the routes for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.include_router(user_router)
    app.include_router(logging_router)
