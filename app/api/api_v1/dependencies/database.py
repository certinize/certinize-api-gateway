import starlite
from sqlalchemy.ext.asyncio import engine

from app.db import crud


async def get_db_engine(state: starlite.State):
    if isinstance(state.engine, engine.AsyncEngine):
        return state.engine
    else:
        raise TypeError(
            "sqlalchemy.ext.asyncio.engine.AsyncEngine is missing from starlite.State"
        )


async def get_db_impl(state: starlite.State):
    db_engine = await get_db_engine(state)
    return crud.DatabaseImpl(db_engine)
