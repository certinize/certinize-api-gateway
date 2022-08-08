import typing
import uuid

import pydantic
import starlite

from app.api.api_v1.dependencies import database
from app.api.api_v1.routes.services import configuration as service
from app.db import crud
from app.models.domain import configuration
from app.models.schemas import configurations


class ConfigurationController(starlite.Controller):
    path = "/configurations"

    dependencies: typing.Optional[dict[str, "starlite.Provide"]] = {
        "configuration_service": starlite.Provide(service.ConfigurationService),
        "database": starlite.Provide(database.get_db_impl),
        "certificate_config_schema": starlite.Provide(
            database.get_certificate_config_schema
        ),
    }

    @starlite.post()
    async def create_template_config(
        self,
        data: configuration.TemplateConfiguration,
        database: crud.DatabaseImpl,
        configuration_service: service.ConfigurationService,
        certificate_config_schema: type[configurations.TemplateConfiguration],
    ) -> dict[str, uuid.UUID | typing.Any]:
        certificate_config = await configuration_service.create_template_config(
            data, certificate_config_schema, database
        )

        return certificate_config

    @starlite.get(path="/{template_config_id:uuid}")
    async def get_template_config(
        self,
        template_config_id: pydantic.UUID1,
        database: crud.DatabaseImpl,
        configuration_service: service.ConfigurationService,
        certificate_config_schema: type[configurations.TemplateConfiguration],
    ) -> typing.Any:

        return template_config_id

    @starlite.get()
    async def list_template_config(self) -> typing.Any:
        return {}
