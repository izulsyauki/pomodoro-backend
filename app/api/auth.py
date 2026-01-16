from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    UserUpdateRequest,
    UserResponse,
    TokenResponse,
    LoginResponse,
    MessageResponse,
    RefreshTokenRequest,
)
from app.services.user_service import AuthService, UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    """Register a new user account."""
    service = AuthService(db)
    return service.register(request)


@router.post("/login", response_model=LoginResponse)
def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and get access tokens."""
    service = AuthService(db)
    return service.login(request)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token using refresh token."""
    service = AuthService(db)
    return service.refresh_tokens(request.refresh_token)


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current authenticated user's profile."""
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
def update_current_user_profile(
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current authenticated user's profile."""
    service = UserService(db)
    return service.update_profile(current_user.id, request)


@router.get("/profile/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    """Get user profile by ID (public endpoint)."""
    from uuid import UUID

    service = UserService(db)
    return service.get_profile(UUID(user_id))


@router.post("/logout", response_model=MessageResponse)
def logout(current_user: User = Depends(get_current_user)):
    """Logout current user (stateless - client should discard token)."""
    return MessageResponse(message="Successfully logged out")
