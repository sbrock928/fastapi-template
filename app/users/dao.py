"""
Data Access Object (DAO) implementation for the User domain.

This module defines the `UserDAO`, which provides async persistence methods
for user-related operations. It extends the generic `BaseDAO` to inherit
CRUD capabilities and serves as the foundation for more complex user-specific
queries and database interactions.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.base_dao import BaseDAO
from app.users.models import UserModel
from app.users.schemas import UserCreate, UserUpdate


class UserDAO(BaseDAO[UserModel, UserCreate, UserUpdate]):
    """
    Async DAO for the User domain.

    Inherits all CRUD methods from BaseDAO and provides a centralized point
    for future user-specific persistence operations, such as:

    - `get_by_email(email: str)`
    - `get_active_users()`
    - `search_users(...)`

    Args:
        session (AsyncSession): SQLAlchemy async session injected via dependency.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_class=UserModel)
