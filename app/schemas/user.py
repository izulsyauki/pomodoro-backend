from datetime import datetime
from typing import Optional
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    """User role enumeration."""

    USER = "user"
    ADMIN = "admin"
    PREMIUM = "premium"


# Request Schemas
class UserRegisterRequest(BaseModel):
    """Schema for user registration request."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)


class UserLoginRequest(BaseModel):
    """Schema for user login request."""

    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    """Schema for updating user profile."""

    full_name: Optional[str] = Field(None, max_length=255)
    avatar_url: Optional[str] = Field(None, max_length=500)


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""

    refresh_token: str


# Response Schemas
class UserResponse(BaseModel):
    """Schema for user response."""

    id: UUID
    email: str
    username: str
    full_name: Optional[str]
    avatar_url: Optional[str]
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginResponse(BaseModel):
    """Schema for login response."""

    user: UserResponse
    tokens: TokenResponse


class MessageResponse(BaseModel):
    """Schema for simple message response."""

    message: str
    success: bool = True
