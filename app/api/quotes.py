from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.schemas.quote import QuoteCreate, QuoteUpdate, QuoteResponse
from app.services.quote_service import QuoteService
from typing import List
from uuid import UUID

router = APIRouter(prefix="/quotes", tags=["Quotes"])


@router.post("/", response_model=QuoteResponse, status_code=201)
def create_quote(
    request: QuoteCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    service = QuoteService(db)
    return service.create(request, user_id=current_admin.id)


@router.get("/", response_model=List[QuoteResponse])
def read_quotes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = QuoteService(db)
    return service.get_all(skip, limit)


@router.get("/{quote_id}", response_model=QuoteResponse)
def read_quote(quote_id: UUID, db: Session = Depends(get_db)):
    service = QuoteService(db)
    return service.get_by_id(quote_id)


@router.put("/{quote_id}", response_model=QuoteResponse)
def update_quote(
    quote_id: UUID,
    request: QuoteUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    service = QuoteService(db)
    return service.update(quote_id, request)


@router.delete("/{quote_id}", status_code=status.HTTP_200_OK)
def delete_quote(
    quote_id: UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    service = QuoteService(db)
    service.delete(quote_id)
    return {"message": "Quote deleted successfully"}
