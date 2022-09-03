from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


logger.info("Connected to database")
Base = declarative_base()



def get_session_factory(database_url: str):
    engine = create_async_engine(database_url, future=True)
    session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    return session_factory


