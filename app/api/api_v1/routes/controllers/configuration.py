import typing
import uuid

import pydantic
import starlite
from sqlalchemy.ext import asyncio as sqlalchemy_asyncio

from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.routes.services import configuration as service
from app.core import abc
from app.models.domain import configuration
from app.models.schemas import configurations, fonts, templates

ListTemplateConfig: typing.TypeAlias = dict[str, list[dict[str, dict[str, typing.Any]]]]


class ConfigurationController(starlite.Controller):
    path = "/configurations"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "engine": starlite.Provide(database_deps.get_db_engine),
        "configs_schema": starlite.Provide(
            database_deps.get_certificate_configs_schema
        ),
        "configuration_service": starlite.Provide(service.ConfigurationService),
        "database": starlite.Provide(database_deps.get_configurations_repository),
        "fonts_schema": starlite.Provide(database_deps.get_fonts_schema),
        "templates_schema": starlite.Provide(database_deps.get_templates_schema),
    }

    @starlite.post()
    async def create_template_config(  # pylint: disable=R0913
        self,
        configs_schema: type[configurations.Configurations],
        configuration_service: service.ConfigurationService,
        data: configuration.TemplateConfiguration,
        database: abc.Database,
        engine: sqlalchemy_asyncio.AsyncEngine,
    ) -> dict[str, uuid.UUID | typing.Any]:
        return await configuration_service.create_template_config(
            configs_schema=configs_schema, data=data, database=database, engine=engine
        )

    @starlite.get(path="/{template_config_id:uuid}")
    async def get_template_config(  # pylint: disable=R0913
        self,
        configs_schema: type[configurations.Configurations],
        configuration_service: service.ConfigurationService,
        database: abc.Database,
        engine: sqlalchemy_asyncio.AsyncEngine,
        fonts_schema: type[fonts.Fonts],
        template_config_id: pydantic.UUID1,
        templates_schema: type[templates.Templates],
    ) -> dict[str, typing.Any]:
        return await configuration_service.get_template_config(
            configs_schema=configs_schema,
            database=database,
            engine=engine,
            fonts_schema=fonts_schema,
            template_config_id=template_config_id,
            templates_schema=templates_schema,
        )

    @starlite.get()
    async def list_template_config(  # pylint: disable=R0913
        self,
        configs_schema: type[configurations.Configurations],
        configuration_service: service.ConfigurationService,
        database: abc.Database,
        engine: sqlalchemy_asyncio.AsyncEngine,
        fonts_schema: type[fonts.Fonts],
        templates_schema: type[templates.Templates],
    ) -> ListTemplateConfig:
        return await configuration_service.list_template_config(
            configs_schema=configs_schema,
            database=database,
            engine=engine,
            fonts_schema=fonts_schema,
            templates_schema=templates_schema,
        )
