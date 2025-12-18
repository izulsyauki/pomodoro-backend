from app.core.security import hash_password, verify_password
from app.repositories.user_repo import UserRepository
from app.utils.tokens import create_access_token, create_refresh_token


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        
    async def register_user(self, email: str, password: str, full_name: str | None = None):
        existing = await self.repo.get_by_email(email)
        if existing:
            raise ValueError("User already exists")
        hashed_password = hash_password(password)
        user = await self.repo.create(email, hashed_password, full_name)
        return user
    
    async def authenticate_user(self, email: str, password: str):
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }