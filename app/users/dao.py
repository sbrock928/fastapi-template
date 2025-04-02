"""
Async DAO (Data Access Object) for the User domain.
Handles low-level database interactions for the UserModel.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.users.models import UserModel
from app.users.schemas import UserCreate, UserUpdate
from typing import List, Optional


class UserDAO:
    """
    Encapsulates all asynchronous database operations related to UserModel.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, user_id: int) -> Optional[UserModel]:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        return result.scalar_one_or_none()

    async def get_all_users(self, limit: int = 100, offset: int = 0) -> List[UserModel]:
        result = await self.session.execute(select(UserModel).offset(offset).limit(limit))
        return result.scalars().all()

    async def create_user(self, user: UserCreate) -> UserModel:
        db_user = UserModel(**user.model_dump())
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def update_user(self, user_id: int, user: UserUpdate) -> Optional[UserModel]:
        db_user = await self.get_user(user_id)
        if db_user:
            for field, value in user.model_dump(exclude_unset=True).items():
                setattr(db_user, field, value)
            await self.session.commit()
            await self.session.refresh(db_user)
        return db_user

    async def delete_user(self, user_id: int) -> Optional[UserModel]:
        db_user = await self.get_user(user_id)
        if db_user:
            await self.session.delete(db_user)
            await self.session.commit()
        return db_user
