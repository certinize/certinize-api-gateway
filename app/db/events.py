from sqlalchemy.ext.asyncio import create_async_engine

# from sqlmodel import SQLModel
from starlite import State

from app.core.config import settings


async def create_db_engine(state: State) -> None:
    state.pool = create_async_engine(
        settings.database_url, **settings.sqlalchemy_kwargs
    )


async def dispose_db_engine(state: State) -> None:
    await state.pool.dispose()


# async def create_db_tables(state: State) -> None:
#     async with state.pool.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)
