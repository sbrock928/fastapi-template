"""
Async service layer for user domain operations.

This module defines the business logic for user-related interactions,
coordinating data access, validation, and domain-specific behavior.
"""

from app.users.dao import UserDAO
from app.users.models import UserModel
from app.users.schemas import UserCreate, UserUpdate
from app.users.exceptions import UserNotFound
from typing import List


class UserService:
    """
    Provides asynchronous business logic for the User domain.
    """

    def __init__(self, dao: UserDAO):
        self.dao = dao

    async def get_user(self, user_id: int) -> UserModel:
        user = await self.dao.get_user(user_id)
        if not user:
            raise UserNotFound()
        return user

    async def get_all_users(self, limit: int = 100, offset: int = 0) -> List[UserModel]:
        return await self.dao.get_all_users(limit=limit, offset=offset)

    async def create_user(self, user: UserCreate) -> UserModel:
        return await self.dao.create_user(user)

    async def update_user(self, user_id: int, user: UserUpdate) -> UserModel:
        updated_user = await self.dao.update_user(user_id, user)
        if not updated_user:
            raise UserNotFound()
        return updated_user

    async def delete_user(self, user_id: int) -> UserModel:
        deleted_user = await self.dao.delete_user(user_id)
        if not deleted_user:
            raise UserNotFound()
        return deleted_user
