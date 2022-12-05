from database import async_db_session
from database.managers import UsersDBManager


async def get_users_manager() -> UsersDBManager:
    async with async_db_session() as session:
        async with session.begin():
            yield UsersDBManager(session)
