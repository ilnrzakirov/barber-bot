from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker


def asinc_engine(url: URL | str) -> AsyncEngine:
    """
        Асинхронный движок БД
    """
    return create_async_engine(url=url, echo=True, encoding="utf-8", pool_pre_ping=True)


async def proceed_schemas(engin: AsyncEngine, metadata) -> None:
    ...
    # async with engin.begin() as conn:
    #     await conn.run_sync(metadata.create_all)


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
