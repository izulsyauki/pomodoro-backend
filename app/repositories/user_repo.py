from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_by_email(self, email: str):
        q = await self.db.execute(select(User).where(User.email == email))
        return q.scalars().first()
    
    async def create(self, email: str, hashed_password: str, full_name: str | None = None):
        new_user = User(email=email, hashed_password=hashed_password, full_name=full_name)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
    
    async def get_by_id(self, user_id: int) -> User | None:
        q = await self.db.execute(select(User).where(User.id == user_id))
        return q.scalars().first()
