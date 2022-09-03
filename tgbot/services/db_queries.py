from datetime import date

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.orm import sessionmaker

from tgbot.models.tables import User


class Db:
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory
        self._session: AsyncSession

    async def async_init(self):
        async with self._session_factory() as session:
            self._session = session

    async def add_user(self, user_id: int, subscribe: date | None = None):
        self._session.add(User(user_id=user_id, subscribe=subscribe))
        try:
            await self._session.commit()
        except (IntegrityError, DBAPIError):
            await self._session.rollback()
            # raise CantAddUser

