import starlite
from sqlalchemy.ext.asyncio import engine

from app.db import crud
from app.models.schemas import configurations, templates, users


async def get_db_engine(state: starlite.State):
    if isinstance(state.engine, engine.AsyncEngine):
        return state.engine

    raise TypeError(
        "sqlalchemy.ext.asyncio.engine.AsyncEngine is missing from starlite.State"
    )


async def get_db_impl(state: starlite.State):
    db_engine = await get_db_engine(state)
    return crud.DatabaseImpl(db_engine)


def get_solana_user_schema():
    return users.SolanaUsers


def get_certificate_config_schema():
    return configurations.TemplateConfigurations


def get_template_schema():
    return templates.Templates
