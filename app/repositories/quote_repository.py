from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.quote import QuoteCreate, QuoteUpdate
from app.models.quote import Quote


class QuoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Quote).offset(skip).limit(limit).all()

    def get_by_id(self, quote_id: UUID):
        return self.db.query(Quote).filter(Quote.id == quote_id).first()

    def create(self, quote: QuoteCreate, user_id: UUID):
        db_quote = Quote(content=quote.content, author=quote.author, created_by=user_id)
        self.db.add(db_quote)
        self.db.commit()
        self.db.refresh(db_quote)
        return db_quote

    def update(self, db_quote: Quote, quote_update: QuoteUpdate):
        update_data = quote_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_quote, key, value)
        self.db.add(db_quote)
        self.db.commit()
        self.db.refresh(db_quote)
        return db_quote

    def delete(self, db_quote: Quote):
        self.db.delete(db_quote)
        self.db.commit()
