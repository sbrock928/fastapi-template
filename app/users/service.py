"""
Async service layer for user domain operations.

This module contains the UserService class, which encapsulates the business logic
for user-related operations. It acts as an intermediary between the web layer
(routes/controllers) and the data access layer (DAO), ensuring consistent
application logic, error handling, and validation coordination.
"""

from typing import List
from app.users.dao import UserDAO
from app.users.models import UserModel
from app.users.schemas import UserCreate, UserUpdate
from app.users.exceptions import UserNotFound


class UserService:
    """
    Provides asynchronous business logic for the User domain.

    Responsibilities:
    - Orchestrates calls to the UserDAO.
    - Applies domain-specific validation and rules.
    - Raises domain-specific exceptions to signal business errors.
    """

    def __init__(self, dao: UserDAO):
        """
        Initializes the UserService with a given UserDAO.

        Args:
            dao (UserDAO): The data access object used to interact with the database.
        """
        self.dao = dao

    async def get_user(self, user_id: int) -> UserModel:
        """
        Retrieve a single user by ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            UserModel: The user with the specified ID.

        Raises:
            UserNotFound: If no user with the given ID exists.
        """
        user = await self.dao.get(user_id)
        if not user:
            raise UserNotFound()
        return user

    async def get_all_users(self, limit: int = 100, offset: int = 0) -> List[UserModel]:
        """
        Retrieve a paginated list of users.

        Args:
            limit (int, optional): Maximum number of users to return. Defaults to 100.
            offset (int, optional): Number of records to skip. Defaults to 0.

        Returns:
            List[UserModel]: A list of user records.
        """
        return await self.dao.get_all(limit=limit, offset=offset)

    async def create_user(self, user: UserCreate) -> UserModel:
        """
        Create a new user from validated input data.

        Args:
            user (UserCreate): A Pydantic schema representing the new user.

        Returns:
            UserModel: The newly created user record.
        """
        return await self.dao.create(user)

    async def update_user(self, user_id: int, user: UserUpdate) -> UserModel:
        """
        Update an existing user's data.

        Args:
            user_id (int): The ID of the user to update.
            user (UserUpdate): A Pydantic schema containing updated fields.

        Returns:
            UserModel: The updated user record.

        Raises:
            UserNotFound: If no user with the given ID exists.
        """
        updated_user = await self.dao.update(user_id, user)
        if not updated_user:
            raise UserNotFound()
        return updated_user

    async def delete_user(self, user_id: int) -> UserModel:
        """
        Delete a user by ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            UserModel: The deleted user record.

        Raises:
            UserNotFound: If no user with the given ID exists.
        """
        deleted_user = await self.dao.delete(user_id)
        if not deleted_user:
            raise UserNotFound()
        return deleted_user
