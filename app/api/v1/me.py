from fastapi import APIRouter, Depends
from app.api.v1.deps import get_current_user

router = APIRouter(prefix="/me", tags=["me"])

@router.get("/", response_model=dict)
async def read_me(current_user=Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "full_name": current_user.full_name}