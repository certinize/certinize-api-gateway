import starlite
from sqlalchemy.ext.asyncio import engine

from app.db import crud
from app.models.schemas import certificates, configurations, fonts, templates, users


async def get_db_engine(state: starlite.State):
    if isinstance(state.engine, engine.AsyncEngine):
        return state.engine

    raise TypeError(
        "sqlalchemy.ext.asyncio.engine.AsyncEngine is missing from starlite.State"
    )


async def get_db_impl(state: starlite.State):
    db_engine = await get_db_engine(state)
    return crud.DatabaseImpl(db_engine)


def get_solana_users_schema() -> type[users.SolanaUsers]:
    return users.SolanaUsers


def get_certificate_configs_schema():
    return configurations.Configurations


def get_templates_schema() -> type[templates.Templates]:
    return templates.Templates


def get_fonts_schema() -> type[fonts.Fonts]:
    return fonts.Fonts


def get_certificate_collections_schema() -> type[certificates.Certificates]:
    return certificates.Certificates
