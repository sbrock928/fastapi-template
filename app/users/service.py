"""
Business logic layer for the User domain.

This module coordinates the core domain logic for users, connecting data access
(DAO), schema validation (Pydantic), and model persistence (SQLAlchemy).

Responsibilities:
- Manages workflows involving user creation, retrieval, update, and deletion.
- Enforces domain rules and orchestrates DAO behavior.
- Provides a clear interface between route handlers and the persistence layer.
"""

from app.users.dao import UserDAO
from app.users.models import UserModel
from app.users.schemas import UserCreate, UserUpdate
from app.users.exceptions import UserNotFound


class UserService:
    """
    A service class for managing user-related operations.
    """

    def __init__(self, dao: UserDAO):
        """
        Initializes the service with a user DAO.

        Args:
            dao (UserDAO): The DAO responsible for user database access.
        """
        self.dao = dao

    def get_user(self, user_id: int) -> UserModel:
        """
        Retrieves a user by ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            UserModel: The user object.

        Raises:
            UserNotFound: If no user with the given ID exists.
        """
        user = self.dao.get_user(user_id)
        if not user:
            raise UserNotFound()
        return user

    def get_all_users(self) -> list[UserModel]:
        """
        Retrieves all users.

        Returns:
            list[UserModel]: All user records in the database.
        """
        return self.dao.get_all_users()

    def create_user(self, user: UserCreate) -> UserModel:
        """
        Creates a new user from validated input.

        Args:
            user (UserCreate): Data for the new user.

        Returns:
            UserModel: The newly created user object.
        """
        return self.dao.create_user(user)

    def update_user(self, user_id: int, user: UserUpdate) -> UserModel:
        """
        Updates an existing user by ID.

        Args:
            user_id (int): The ID of the user to update.
            user (UserUpdate): Data with updated fields.

        Returns:
            UserModel: The updated user object.

        Raises:
            UserNotFound: If no user with the given ID exists.
        """
        updated_user = self.dao.update_user(user_id, user)
        if not updated_user:
            raise UserNotFound()
        return updated_user

    def delete_user(self, user_id: int) -> UserModel:
        """
        Deletes a user by ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            UserModel: The deleted user object.

        Raises:
            UserNotFound: If no user with the given ID exists.
        """
        deleted_user = self.dao.delete_user(user_id)
        if not deleted_user:
            raise UserNotFound()
        return deleted_user
