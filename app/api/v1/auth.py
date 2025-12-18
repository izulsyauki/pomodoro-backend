from fastapi import APIRouter, Depends, HTTPException, status
from app.api.v1.deps import get_db
from app.repositories.user_repo import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
async def register(payload: RegisterRequest, db=Depends(get_db)):
    repo = UserRepository(db)
    svc = AuthService(repo)
    user = await svc.register(payload.email, payload.password, payload.full_name)
    tokens = await svc.authenticate(payload.email, payload.password)
    return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"], "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db=Depends(get_db)):
    repo = UserRepository(db)
    svc = AuthService(repo)
    tokens = await svc.authenticate(payload.email, payload.password)
    if not tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"], "token_type": "bearer"}
        