from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class QuoteBase(BaseModel):
    content: str
    author: str


class QuoteCreate(QuoteBase):
    pass


class QuoteUpdate(BaseModel):
    content: Optional[str] = None
    author: Optional[str] = None


class QuoteResponse(QuoteBase):
    id: UUID
    created_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
