import uuid
from typing import List, Optional

from sqlalchemy import delete, select, update, and_
from sqlalchemy.orm import Session

from database.db_models import UserDBModel


class UsersDBManager:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    async def create(
        self, username: str, password: str, name: str, surname: str, age: Optional[int]
    ) -> UserDBModel:
        new_user = UserDBModel(
            id=str(uuid.uuid4()),
            username=username,
            password=password,
            name=name,
            surname=surname,
            age=age,
        )
        self._db_session.add(new_user)
        await self.__commit_to_db()
        return new_user

    async def get(self, user_id: str) -> Optional[UserDBModel]:
        return await self._db_session.get(UserDBModel, user_id)

    async def list(self) -> List[UserDBModel]:
        result = await self._db_session.execute(select(UserDBModel))
        return result.scalars().all()

    async def find(self, **kwargs) -> List[UserDBModel]:
        query = select(UserDBModel).where(self.__create_where_stmt(kwargs))
        result = await self._db_session.execute(query)
        return result.scalars().all()

    async def update(self, user_id: str, **kwargs):
        query = update(UserDBModel).where(UserDBModel.id == user_id)
        query = query.values(**kwargs)
        await self._db_session.execute(query)

    async def delete(self, user_id: str):
        query = delete(UserDBModel).where(UserDBModel.id == user_id)
        await self._db_session.execute(query)
        await self.__commit_to_db()

    async def __commit_to_db(self):
        await self._db_session.flush()
        await self._db_session.commit()

    def __create_where_stmt(self, params: dict):
        conditions = []
        for key, value in params.items():
            conditions.append(getattr(UserDBModel, key) == value)
        return and_(*conditions)
