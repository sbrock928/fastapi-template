"""
API routes for the User domain.

This module defines RESTful endpoints for creating, retrieving,
updating, and deleting user resources. It connects the FastAPI
routing layer to the service layer and ensures consistent
validation and error handling.
"""

from fastapi import APIRouter
from app.users.schemas import UserCreate, UserResponse, UserUpdate
from app.users.service import UserService
from app.core.exceptions import NoContent
from app.users.dao import UserDAO
from app.core.database import SessionDep
from app.users.models import UserModel

router = APIRouter(tags=["users"])


@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db_session: SessionDep) -> UserModel:
    """
    Create a new user.

    Args:
        user_data (UserCreate): Data for the new user.
        db_session (SessionDep): Active DB session.

    Returns:
        UserResponse: The newly created user.
    """
    service = UserService(UserDAO(db_session))
    return service.create_user(user_data)


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db_session: SessionDep) -> UserResponse:
    """
    Retrieve a user by ID.

    Args:
        user_id (int): The ID of the user.
        db_session (SessionDep): Active DB session.

    Returns:
        UserModel: The user object.

    Raises:
        UserNotFound: If no user exists with the provided ID.
    """
    service = UserService(UserDAO(db_session))
    return service.get_user(user_id)


@router.get("/users", response_model=list[UserResponse], responses={204: {}})
def get_all_users(db_session: SessionDep) -> list[UserModel]:
    """
    Retrieve all users.

    Args:
        db_session (SessionDep): Active DB session.

    Returns:
        list[UserModel]: A list of all users.

    Raises:
        NoContent: If no users are found.
    """
    service = UserService(UserDAO(db_session))
    users = service.get_all_users()
    if not users:
        raise NoContent()
    return users


@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db_session: SessionDep) -> UserModel:
    """
    Update a user by ID.

    Args:
        user_id (int): ID of the user to update.
        user_data (UserUpdate): Fields to update.
        db_session (SessionDep): Active DB session.

    Returns:
        UserModel: The updated user.

    Raises:
        UserNotFound: If the user does not exist.
    """
    service = UserService(UserDAO(db_session))
    return service.update_user(user_id, user_data)


@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db_session: SessionDep) -> UserModel:
    """
    Delete a user by ID.

    Args:
        user_id (int): ID of the user to delete.
        db_session (SessionDep): Active DB session.

    Returns:
        UserModel: The deleted user.

    Raises:
        UserNotFound: If the user does not exist.
    """
    service = UserService(UserDAO(db_session))
    return service.delete_user(user_id)
