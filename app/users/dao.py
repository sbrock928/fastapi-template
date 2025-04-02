"""
Data Access Object (DAO) for user-related database operations.

This module provides an abstraction layer for querying, creating, updating,
and deleting user records from the database. It decouples direct database access
from business logic and ensures that all interactions are performed consistently
and safely.
"""

from sqlalchemy.orm import Session
from app.users.models import UserModel
from app.users.schemas import UserCreate, UserUpdate


class UserDAO:
    """
    Provides CRUD operations for the UserModel entity.
    """

    def __init__(self, db_session: Session):
        """
        Initializes the UserDAO with a SQLAlchemy session.

        Args:
            db_session (Session): The active database session.
        """
        self.db = db_session

    def get_user(self, user_id: int) -> UserModel | None:
        """
        Retrieves a single user by ID.

        Args:
            user_id (int): The user's unique identifier.

        Returns:
            UserModel | None: The matching user or None if not found.
        """
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_all_users(self) -> list[UserModel]:
        """
        Retrieves all users in the database.

        Returns:
            list[UserModel]: A list of all user records.
        """
        return self.db.query(UserModel).all()

    def create_user(self, user: UserCreate) -> UserModel:
        """
        Creates and persists a new user in the database.

        Args:
            user (UserCreate): The user data to insert.

        Returns:
            UserModel: The newly created user with an assigned ID.
        """
        db_user = UserModel(**user.model_dump())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user: UserUpdate) -> UserModel | None:
        """
        Updates an existing user.

        Args:
            user_id (int): The ID of the user to update.
            user (UserUpdate): The fields to update.

        Returns:
            UserModel | None: The updated user, or None if not found.
        """
        db_user = self.get_user(user_id)
        if db_user:
            for field, value in user.model_dump(exclude_unset=True).items():
                setattr(db_user, field, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> UserModel | None:
        """
        Deletes a user by ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            UserModel | None: The deleted user, or None if not found.
        """
        db_user = self.get_user(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return db_user
