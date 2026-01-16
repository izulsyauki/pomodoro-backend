from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.repositories.pomodoro_repository import PomodoroRepository
from app.schemas.pomodoro import (
    PomodoroSessionCreate,
    PomodoroSessionResponse,
    LeaderboardEntry,
)


class PomodoroService:
    """Service for pomodoro operations."""

    def __init__(self, db: Session):
        self.repository = PomodoroRepository(db)

    def create_session(
        self, user_id: UUID, session_data: PomodoroSessionCreate
    ) -> PomodoroSessionResponse:
        """Create a new pomodoro session."""
        session = self.repository.create(user_id, session_data)
        return PomodoroSessionResponse.model_validate(session)

    def get_history(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[PomodoroSessionResponse]:
        """Get pomodoro history for a user."""
        sessions = self.repository.get_by_user_id(user_id, skip, limit)
        # Manually map to handle any custom logic if needed, or just model_validate
        return [PomodoroSessionResponse.model_validate(s) for s in sessions]

    def get_leaderboard(self, limit: int = 10) -> List[LeaderboardEntry]:
        """Get leaderboard."""
        return self.repository.get_leaderboard(limit)
