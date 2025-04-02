"""
Pydantic schemas for user creation, update, and response.

These schemas enforce validation rules and structure for user-related
operations, including input validation and output serialization.
"""

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., max_length=255)

    model_config = ConfigDict(from_attributes=True, strict=True, extra="forbid")


class UserCreate(UserBase):
    """Schema for creating a new user."""

    pass


class UserResponse(UserBase):
    """Schema for returning user data."""

    id: int


class UserUpdate(BaseModel):
    """Schema for updating user details."""

    first_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = Field(default=None, max_length=255)

    model_config = ConfigDict(from_attributes=True, strict=True, extra="forbid")
