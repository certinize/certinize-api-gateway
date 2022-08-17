import typing

import starlite
from starlette import datastructures

from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.dependencies import image_processor as image_processor_deps
from app.api.api_v1.routes.services import template as template_svcs
from app.db import crud
from app.models.schemas import templates
from app.services import image_processor


class TemplateController(starlite.Controller):
    path = "/templates"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "database": starlite.Provide(database_deps.get_db_impl),
        "image_processor_": starlite.Provide(
            image_processor_deps.get_image_processor_client
        ),
        "template_service": starlite.Provide(template_svcs.TemplateService),
        "templates_schema": starlite.Provide(database_deps.get_template_schema),
    }

    @starlite.post()
    async def add_certificate_template(  # pylint: disable=R0913
        self,
        database: crud.DatabaseImpl,
        image_processor_: image_processor.ImageProcessor,
        template_service: template_svcs.TemplateService,
        templates_schema: type[templates.Templates],
        data: dict[
            str, datastructures.UploadFile | list[datastructures.UploadFile]
        ] = starlite.Body(media_type=starlite.RequestEncodingType.MULTI_PART),
    ) -> typing.Any:
        return await template_service.add_certificate_template(
            data=data,
            database=database,
            image_processor_=image_processor_,
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
