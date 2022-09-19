import typing

import starlite
from starlette import datastructures

from app.api.api_v1.dependencies import associated_services
from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.routes.services import template as template_svcs
from app.db import crud
from app.models.schemas import templates
from app.services import object_processor


class TemplateController(starlite.Controller):
    path = "/templates"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "database": starlite.Provide(database_deps.get_db_impl),
        "object_processor_": starlite.Provide(
            associated_services.get_object_processor_client
        ),
        "template_service": starlite.Provide(template_svcs.TemplateService),
        "templates_schema": starlite.Provide(database_deps.get_templates_schema),
    }

    @starlite.post()
    async def add_certificate_template(  # pylint: disable=R0913
        self,
        database: crud.DatabaseImpl,
        object_processor_: object_processor.ObjectProcessor,
        template_service: template_svcs.TemplateService,
        templates_schema: type[templates.Templates],
        data: dict[
            str, datastructures.UploadFile | list[datastructures.UploadFile]
        ] = starlite.Body(media_type=starlite.RequestEncodingType.MULTI_PART),
    ) -> typing.Any:
        return await template_service.add_certificate_template(
            data=data,
            database=database,
            object_processor_=object_processor_,
            template_schema=templates_schema,
        )

    @starlite.get()
    async def list_certificate_templates(
        self,
        database: crud.DatabaseImpl,
        template_service: template_svcs.TemplateService,
        templates_schema: type[templates.Templates],
    ) -> typing.Any:
        result = await template_service.list_certificate_templates(
            database=database, templates_schema=templates_schema
        )

        return {"templates": result.all()}
