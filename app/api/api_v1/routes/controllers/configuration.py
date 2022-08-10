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
        "database_": starlite.Provide(database.get_db_impl),
        "certificate_config_schema": starlite.Provide(
            database.get_certificate_config_schema
        ),
    }

    @starlite.post()
    async def create_template_config(
        self,
        data: configuration.TemplateConfiguration,
        certificate_config_schema: type[configurations.TemplateConfigurations],
        configuration_service: service.ConfigurationService,
        database_: crud.DatabaseImpl,
    ) -> dict[str, uuid.UUID | typing.Any]:
        return await configuration_service.create_template_config(
            data, certificate_config_schema, database_
        )

    @starlite.get(path="/{template_config_id:uuid}")
    async def get_template_config(
        self,
        template_config_id: pydantic.UUID1,
        certificate_config_schema: type[configurations.TemplateConfigurations],
        configuration_service: service.ConfigurationService,
        database_: crud.DatabaseImpl,
    ) -> typing.Any:
        return await configuration_service.get_template_config(
            template_config_id, certificate_config_schema, database_
        )

    @starlite.get()
    async def list_template_config(
        self,
        certificate_config_schema: type[configurations.TemplateConfigurations],
        configuration_service: service.ConfigurationService,
        database_: crud.DatabaseImpl,
    ) -> typing.Any:
        return await configuration_service.list_template_config(
            certificate_config_schema, database_
        )
