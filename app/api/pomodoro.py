from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.pomodoro import (
    PomodoroSessionCreate,
    PomodoroSessionResponse,
    LeaderboardEntry,
)
from app.services.pomodoro_service import PomodoroService

router = APIRouter(prefix="/pomodoro", tags=["Pomodoro"])
leaderboard_router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.post(
    "/sessions",
    response_model=PomodoroSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_session(
    request: PomodoroSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new pomodoro session."""
    service = PomodoroService(db)
    # The response should include the current user's name if needed, but the schema has it optional
    response = service.create_session(current_user.id, request)
    response.name = current_user.username  # Populate name if needed for history display
    return response


@router.get("/history", response_model=List[PomodoroSessionResponse])
def get_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get pomodoro session history for the current user."""
    service = PomodoroService(db)
    sessions = service.get_history(current_user.id, skip, limit)
    # Populate name for each session (it's the same user)
    for s in sessions:
        s.name = current_user.username
    return sessions


@leaderboard_router.get("/", response_model=List[LeaderboardEntry])
def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    """Get top users by accumulated focus time."""
    service = PomodoroService(db)
    return service.get_leaderboard(limit)
