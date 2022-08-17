import pydantic
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlmodel import SQLModel
from starlite import State

from app.core.config import settings


async def create_db_engine(state: State) -> None:
    assert isinstance(settings.database_url, pydantic.PostgresDsn)
    database_url = settings.database_url.replace("postgres://", "postgresql+asyncpg://")
    state.engine = create_async_engine(database_url, **settings.sqlalchemy_kwargs)


async def dispose_db_engine(state: State) -> None:
    await state.engine.dispose()


async def create_db_tables(state: State) -> None:
    engine = state.engine
    if isinstance(engine, AsyncEngine):
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    else:
        raise TypeError(
            "sqlalchemy.ext.asyncio.engine.AsyncEngine is missing from starlite.State"
        )
