import typing
import uuid

import pydantic
import starlite
from sqlalchemy.ext import asyncio as sqlalchemy_asyncio

from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.routes.services import configuration as service
from app.core import abc
from app.models.domain import configuration

ListTemplateConfig: typing.TypeAlias = dict[str, list[dict[str, dict[str, typing.Any]]]]


class ConfigurationController(starlite.Controller):
    path = "/configurations"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "engine": starlite.Provide(database_deps.get_db_engine),
        "configuration_service": starlite.Provide(service.ConfigurationService),
        "database": starlite.Provide(database_deps.get_configurations_repository),
    }

    @starlite.post()
    async def create_template_config(  # pylint: disable=R0913
        self,
        configuration_service: service.ConfigurationService,
        data: configuration.TemplateConfiguration,
        database: abc.Database,
        engine: sqlalchemy_asyncio.AsyncEngine,
        token: str = starlite.Parameter(header="X-API-KEY", min_length=36),
    ) -> dict[str, uuid.UUID | typing.Any]:
        return await configuration_service.create_template_config(
            data, database, engine, token
        )

    @starlite.get(path="/{template_config_id:uuid}")
    async def get_template_config(  # pylint: disable=R0913
        self,
        configuration_service: service.ConfigurationService,
        database: abc.Database,
        engine: sqlalchemy_asyncio.AsyncEngine,
        template_config_id: pydantic.UUID1,
        token: str = starlite.Parameter(header="X-API-KEY", min_length=36),
    ) -> dict[str, typing.Any]:
        return await configuration_service.get_template_config(
            database, engine, template_config_id, token
        )

    @starlite.get()
    async def list_template_config(  # pylint: disable=R0913
        self,
        configuration_service: service.ConfigurationService,
        database: abc.Database,
        engine: sqlalchemy_asyncio.AsyncEngine,
        token: str = starlite.Parameter(header="X-API-KEY", min_length=36),
    ) -> ListTemplateConfig:
        return await configuration_service.list_template_config(database, engine, token)
