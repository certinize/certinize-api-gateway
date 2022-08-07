import typing
import uuid

import pydantic
import starlite

from app.api.api_v1.dependencies import database
from app.api.api_v1.routes.services import template as service
from app.db import crud
from app.models.domain import template
from app.models.schemas import templates


class TemplateController(starlite.Controller):
    path = "/templates"

    dependencies: typing.Optional[dict[str, "starlite.Provide"]] = {
        "certificate_service": starlite.Provide(service.TemplateService),
        "database": starlite.Provide(database.get_db_impl),
    }

    @starlite.post(
        dependencies={
            "certificate_config_schema": starlite.Provide(
                database.get_certificate_config_schema
            )
        },
    )
    async def create_template_config(
        self,
        data: template.TemplateConfigSave,
        database: crud.DatabaseImpl,
        certificate_service: service.TemplateService,
        certificate_config_schema: type[templates.TemplateConfiguration],
    ) -> dict[str, uuid.UUID | typing.Any]:
        certificate_config = await certificate_service.save(
            data, certificate_config_schema, database
        )

        return certificate_config

    @starlite.get(path="/{template_config_id:uuid}")
    async def get_template_config(
        self,
        template_config_id: pydantic.UUID1,
        database: crud.DatabaseImpl,
        certificate_config_schema: type[templates.TemplateConfiguration],
    ) -> typing.Any:
        return template_config_id
