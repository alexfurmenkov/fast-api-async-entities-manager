from typing import Optional, List

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from database.db_models import UserDBModel


class UsersDBManager:

    def __init__(self, db_session: Session):
        self._db_session = db_session

    async def create(self, username: str, name: str, surname: str, age: Optional[int]) -> UserDBModel:
        new_user = UserDBModel(username, name, surname, age)
        self._db_session.add(new_user)
        await self._db_session.flush()
        return new_user

    async def get(self, user_id: str) -> UserDBModel:
        query = select(UserDBModel).where(UserDBModel.id == user_id)
        result = await self._db_session.execute(query)
        return result.scalars().all()

    async def list(self) -> List[UserDBModel]:
        query = await self._db_session.execute(select(UserDBModel))
        return query.scalars().all()

    async def update(self, user_id: str, **kwargs):
        query = update(UserDBModel).where(UserDBModel.id == user_id)
        query = query.values(**kwargs)
        await self._db_session.execute(query)

    async def delete(self, user_id: str):
        query = delete(UserDBModel).where(UserDBModel.id == user_id)
        await self._db_session.execute(query)
