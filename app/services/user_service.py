from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    UserUpdateRequest,
    UserResponse,
    TokenResponse,
    LoginResponse,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)


class AuthService:
    """Service for authentication operations."""

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def register(self, request: UserRegisterRequest) -> UserResponse:
        """Register a new user."""
        # Check if email already exists
        if self.repository.exists_by_email(request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Check if username already exists
        if self.repository.exists_by_username(request.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
            )

        # Create new user
        user = User(
            email=request.email,
            username=request.username,
            hashed_password=hash_password(request.password),
            full_name=request.full_name,
        )

        created_user = self.repository.create(user)
        return UserResponse.model_validate(created_user)

    def login(self, request: UserLoginRequest) -> LoginResponse:
        """Authenticate user and return tokens."""
        # Get user by email
        user = self.repository.get_by_email(request.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Verify password
        if not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated"
            )

        # Generate tokens
        token_data = {"sub": str(user.id), "email": user.email}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return LoginResponse(
            user=UserResponse.model_validate(user),
            tokens=TokenResponse(
                access_token=access_token, refresh_token=refresh_token
            ),
        )

    def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token."""
        payload = decode_token(refresh_token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
            )

        user_id = payload.get("sub")
        user = self.repository.get_by_id(UUID(user_id))

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        # Generate new tokens
        token_data = {"sub": str(user.id), "email": user.email}
        new_access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)

        return TokenResponse(
            access_token=new_access_token, refresh_token=new_refresh_token
        )


class UserService:
    """Service for user operations."""

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_profile(self, user_id: UUID) -> UserResponse:
        """Get user profile by ID."""
        user = self.repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return UserResponse.model_validate(user)

    def update_profile(self, user_id: UUID, request: UserUpdateRequest) -> UserResponse:
        """Update user profile."""
        user = self.repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Update fields if provided
        if request.full_name is not None:
            user.full_name = request.full_name
        if request.avatar_url is not None:
            user.avatar_url = request.avatar_url

        updated_user = self.repository.update(user)
        return UserResponse.model_validate(updated_user)
