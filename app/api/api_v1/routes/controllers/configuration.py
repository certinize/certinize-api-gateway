import typing
import uuid

import pydantic
import starlite

from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.routes.services import configuration as service
from app.db import crud
from app.models.domain import configuration
from app.models.schemas import configurations, fonts, templates


class ConfigurationController(starlite.Controller):
    path = "/configurations"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "configuration_service": starlite.Provide(service.ConfigurationService),
        "database": starlite.Provide(database_deps.get_db_impl),
        "certificate_config_schema": starlite.Provide(
            database_deps.get_certificate_configs_schema
        ),
    }

    @starlite.post()
    async def create_template_config(
        self,
        data: configuration.TemplateConfiguration,
        certificate_config_schema: type[configurations.Configurations],
        configuration_service: service.ConfigurationService,
        database: crud.DatabaseImpl,
    ) -> dict[str, uuid.UUID | typing.Any]:
        return await configuration_service.create_template_config(
            data, certificate_config_schema, database
        )

    @starlite.get(
        path="/{template_config_id:uuid}",
        dependencies={
            "fonts_schema": starlite.Provide(database_deps.get_fonts_schema),
            "templates_schema": starlite.Provide(database_deps.get_templates_schema),
        },
    )
    async def get_template_config(  # pylint: disable=R0913
        self,
        template_config_id: pydantic.UUID1,
        certificate_config_schema: type[configurations.Configurations],
        fonts_schema: type[fonts.Fonts],
        template_schema: type[templates.Templates],
        configuration_service: service.ConfigurationService,
        database: crud.DatabaseImpl,
    ) -> typing.Any:
        return await configuration_service.get_template_config(
            template_config_id=template_config_id,
            certificate_config_schema=certificate_config_schema,
            templates_schema=template_schema,
            fonts_schema=fonts_schema,
            database=database,
        )

    @starlite.get(
        dependencies={
            "fonts_schema": starlite.Provide(database_deps.get_fonts_schema),
            "templates_schema": starlite.Provide(database_deps.get_templates_schema),
        }
    )
    async def list_template_config(  # pylint: disable=R0913
        self,
        certificate_config_schema: type[configurations.Configurations],
        fonts_schema: type[fonts.Fonts],
        templates_schema: type[templates.Templates],
        configuration_service: service.ConfigurationService,
        database: crud.DatabaseImpl,
    ) -> typing.Any:
        return await configuration_service.list_template_config(
            certificate_config_schema=certificate_config_schema,
            templates_schema=templates_schema,
            fonts_schema=fonts_schema,
            database=database,
        )
