from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field


# Request Schemas
class PomodoroSessionCreate(BaseModel):
    """Schema for creating a pomodoro session."""

    focus_count: int = Field(default=0, ge=0)
    focus_time: int = Field(..., ge=0, description="Focus time in seconds")
    break_time: int = Field(default=0, ge=0, description="Break time in seconds")
    long_break_time: int = Field(
        default=0, ge=0, description="Long break time in seconds"
    )
    status: str = Field(default="completed")


# Response Schemas
class PomodoroSessionResponse(BaseModel):
    """Schema for pomodoro session response."""

    id: UUID
    user_id: UUID
    # optional name in case we want to embed it, though history usually just needs session info
    name: Optional[str] = None

    focus_count: int
    focus_time: int
    break_time: int
    long_break_time: int
    status: str

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LeaderboardEntry(BaseModel):
    """Schema for leaderboard entry."""

    user_id: UUID
    username: str
    avatar_url: Optional[str] = None
    total_focus_time: int  # Total seconds
    total_sessions: int
