import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class PomodoroSession(Base):
    """Pomodoro Session database model."""

    __tablename__ = "pomodoro_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )

    # We can perform a join to get user name for history/leaderboard
    user = relationship("User", backref="pomodoro_sessions")

    focus_count = Column(Integer, default=0)
    focus_time = Column(Integer, default=0)  # In seconds
    break_time = Column(Integer, default=0)  # In seconds
    long_break_time = Column(Integer, default=0)  # In seconds
    status = Column(String(50), default="completed")  # completed, cancelled, etc.

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PomodoroSession(id={self.id}, user_id={self.user_id}, status={self.status})>"
