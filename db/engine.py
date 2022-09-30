from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker


def asinc_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine(url=url, echo=True, encoding="utf-8", pool_pre_ping=True)


async def proceed_schemas(engin: AsyncEngine, metadata) -> None:
    async with engin.connect() as conn:
        await conn.run_sync(metadata.create_all)


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession)
