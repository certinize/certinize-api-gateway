import starlite
from sqlalchemy.ext.asyncio import engine

from app.db import crud
from app.db.repositories import configurations as configurations_repository
from app.db.repositories import templates as templates_repository
from app.models.schemas import certificates, configurations, fonts, templates, users


def get_db_engine(state: starlite.State):
    if isinstance(state.engine, engine.AsyncEngine):
        return state.engine

    raise TypeError(
        "sqlalchemy.ext.asyncio.engine.AsyncEngine is missing from starlite.State"
    )


def get_db_impl(state: starlite.State):
    db_engine = get_db_engine(state)
    return crud.DatabaseImpl(db_engine)


def get_configurations_repository():
    return configurations_repository.ConfigurationsRepository()


def get_templates_repository():
    return templates_repository.TemplatesRepository()


def get_solana_users_schema() -> type[users.SolanaUsers]:
    return users.SolanaUsers


def get_vequest_schema() -> type[users.VerificationRequests]:
    return users.VerificationRequests


def get_certificate_configs_schema():
    return configurations.Configurations


def get_templates_schema() -> type[templates.Templates]:
    return templates.Templates


def get_fonts_schema() -> type[fonts.Fonts]:
    return fonts.Fonts


def get_certificate_collections_schema() -> type[certificates.Certificates]:
    return certificates.Certificates
