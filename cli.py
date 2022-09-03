import asyncio

from sqlalchemy.ext.asyncio import create_async_engine

from tgbot.config import get_settings
from tgbot.models import tables
from tgbot.services.db_connection import Base


settings = get_settings()
engine = create_async_engine(settings.db_url, future=True)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_models())

