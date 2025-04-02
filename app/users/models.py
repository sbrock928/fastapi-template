"""
SQLAlchemy model(s) for the Users domain.
"""

from sqlalchemy import Column, Integer, String
from app.core.database import Base


class UserModel(Base):
    """
    Represents a User entity in the database.

    Attributes:
        id (int): Primary key of the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email address of the user (must be unique).
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
