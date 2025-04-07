"""
Asynchronous API routes for the User domain.
Includes OpenAPI documentation, pagination, and dependency injection.
"""

from fastapi import APIRouter, Depends, Query
from app.users.schemas import UserCreate, UserResponse, UserUpdate
from app.users.service import UserService
from app.users.dao import UserDAO
from app.core.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(session: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(UserDAO(session))


@router.post("", response_model=UserResponse, status_code=201, summary="Create a new user")
async def create_user(
    user_data: UserCreate, service: UserService = Depends(get_user_service)
) -> Any:
    """Create a new user with the provided data."""
    return await service.create_user(user_data)


@router.get("/{user_id}", response_model=UserResponse, summary="Get user by ID")
async def get_user(user_id: int, service: UserService = Depends(get_user_service)) -> Any:
    """Retrieve a user by their unique ID."""
    return await service.get_user(user_id)


@router.get("", response_model=list[UserResponse], summary="List all users")
async def get_all_users(
    limit: int = Query(100, le=1000, description="Maximum users to return"),
    offset: int = Query(0, description="Number of users to skip"),
    service: UserService = Depends(get_user_service),
) -> Any:
    """Retrieve a paginated list of users."""
    return await service.get_all_users(limit=limit, offset=offset)


@router.patch("/{user_id}", response_model=UserResponse, summary="Update user by ID")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> Any:
    """Partially update fields for a user by ID."""
    return await service.update_user(user_id, user_data)


@router.delete("/{user_id}", response_model=UserResponse, summary="Delete user by ID")
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)) -> Any:
    """Delete a user by their unique ID."""
    return await service.delete_user(user_id)
