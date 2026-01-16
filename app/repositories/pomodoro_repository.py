from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.pomodoro import PomodoroSession
from app.models.user import User
from app.schemas.pomodoro import PomodoroSessionCreate, LeaderboardEntry


class PomodoroRepository:
    """Repository for pomodoro session operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self, user_id: UUID, session_data: PomodoroSessionCreate
    ) -> PomodoroSession:
        """Create a new pomodoro session."""
        db_session = PomodoroSession(
            user_id=user_id,
            focus_count=session_data.focus_count,
            focus_time=session_data.focus_time,
            break_time=session_data.break_time,
            long_break_time=session_data.long_break_time,
            status=session_data.status,
        )
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session

    def get_by_user_id(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[PomodoroSession]:
        """Get pomodoro sessions for a user."""
        return (
            self.db.query(PomodoroSession)
            .filter(PomodoroSession.user_id == user_id)
            .order_by(desc(PomodoroSession.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_leaderboard(self, limit: int = 10) -> List[LeaderboardEntry]:
        """Get top users by total focus time."""
        # Aggregate focus time by user
        results = (
            self.db.query(
                User.id,
                User.username,
                User.avatar_url,
                func.sum(PomodoroSession.focus_time).label("total_focus_time"),
                func.count(PomodoroSession.id).label("total_sessions"),
            )
            .join(PomodoroSession, User.id == PomodoroSession.user_id)
            .group_by(User.id)
            .order_by(desc("total_focus_time"))
            .limit(limit)
            .all()
        )

        leaderboard = []
        for r in results:
            leaderboard.append(
                LeaderboardEntry(
                    user_id=r.id,
                    username=r.username,
                    avatar_url=r.avatar_url,
                    total_focus_time=r.total_focus_time or 0,
                    total_sessions=r.total_sessions or 0,
                )
            )

        return leaderboard
