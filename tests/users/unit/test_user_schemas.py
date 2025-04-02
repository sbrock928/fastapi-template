"""
Unit tests for user Pydantic schemas.
"""

from pydantic import ValidationError
from app.users.schemas import UserCreate, UserUpdate, UserResponse
from typing import Dict, Any


class TestUserCreateSchema:
    """Unit tests for the UserCreate schema."""

    def test_valid_user_create(self, user_payload: Dict[str, Any]) -> None:
        user = UserCreate(**user_payload)
        assert user.first_name == "Alice"
        assert user.last_name == "Smith"
        assert user.email == "alice@example.com"

    def test_invalid_user_create_missing_email(self) -> None:
        invalid_payload = {"first_name": "Alice", "last_name": "Smith"}
        try:
            UserCreate(**invalid_payload)
        except ValidationError as e:
            assert "email" in str(e)


class TestUserUpdateSchema:
    """Unit tests for the UserUpdate schema."""

    def test_valid_user_update(self, user_payload: Dict[str, Any]) -> None:
        user = UserUpdate(**user_payload)
        assert user.first_name == "Alice"
        assert user.last_name == "Smith"

    def test_partial_user_update(self) -> None:
        user = UserUpdate(last_name="Johnson")
        assert user.last_name == "Johnson"
        assert user.first_name is None


class TestUserResponseSchema:
    """Unit tests for the UserResponse schema."""

    def test_valid_user_response(self, user_response: Dict[str, Any]) -> None:
        user = UserResponse(**user_response)
        assert user.id == 1
        assert user.first_name == "Alice"
        assert user.last_name == "Smith"
        assert user.email == "alice@example.com"
