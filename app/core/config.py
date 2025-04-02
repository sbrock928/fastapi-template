"""
Configuration settings for the application.
"""

import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
TESTING = os.getenv("TESTING", "False").lower() in ("true", "1", "t")
