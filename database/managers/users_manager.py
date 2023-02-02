import uuid
from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from database.db_models import UserDBModel


class UsersDBManager:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    async def create(
        self, username: str, name: str, surname: str, age: Optional[int]
    ) -> UserDBModel:
        new_user = UserDBModel(
            id=str(uuid.uuid4()), username=username, name=name, surname=surname, age=age
        )
        self._db_session.add(new_user)
        await self._db_session.flush()
        return new_user

    async def get(self, user_id: str) -> Optional[UserDBModel]:
        return await self._db_session.get(UserDBModel, user_id)

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
