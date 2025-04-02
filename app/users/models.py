"""
SQLAlchemy model definition for the Users domain.

This module defines the database schema for user entities, including field-level
constraints such as maximum character lengths and uniqueness. It is used by
SQLAlchemy ORM to map Python objects to database records and supports integration
with Pydantic via `from_orm` or `from_attributes`.

Tables:
    - users: Stores user profile information.

Fields:
    - id (int): Auto-incrementing primary key.
    - first_name (str): The user's first name (max 100 characters).
    - last_name (str): The user's last name (max 100 characters).
    - email (str): The user's unique email address (max 255 characters).
"""

from sqlalchemy import Column, Integer, String
from app.core.database import Base


class UserModel(Base):
    """
    ORM model for a user in the system.
    Represents a user record with uniquely identifiable email.

    Attributes:
        id (int): Unique identifier for the user.
        first_name (str): First name, max 100 characters.
        last_name (str): Last name, max 100 characters.
        email (str): Email address, max 255 characters, must be unique.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
