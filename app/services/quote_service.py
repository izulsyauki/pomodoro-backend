from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.quote import QuoteCreate, QuoteUpdate
from app.repositories.quote_repository import QuoteRepository
from fastapi import HTTPException, status


class QuoteService:
    def __init__(self, db: Session):
        self.repository = QuoteRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)

    def get_by_id(self, quote_id: UUID):
        quote = self.repository.get_by_id(quote_id)
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found"
            )
        return quote

    def create(self, quote: QuoteCreate, user_id: UUID):
        return self.repository.create(quote, user_id)

    def update(self, quote_id: UUID, quote_update: QuoteUpdate):
        quote = self.get_by_id(quote_id)
        return self.repository.update(quote, quote_update)

    def delete(self, quote_id: UUID):
        quote = self.get_by_id(quote_id)
        self.repository.delete(quote)
