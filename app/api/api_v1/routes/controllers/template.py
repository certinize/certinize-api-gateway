import typing

import starlite
from starlette import datastructures

from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.dependencies import imagekit as imagekit_deps
from app.api.api_v1.routes.services import template as template_svcs
from app.db import crud
from app.models.schemas import templates
from app.services import imagekit


class TemplateController(starlite.Controller):
    path = "/templates"

    dependencies: typing.Optional[dict[str, "starlite.Provide"]] = {
        "database": starlite.Provide(database_deps.get_db_impl),
        "imagekit_client": starlite.Provide(imagekit_deps.get_imagekit_client),
        "template_service": starlite.Provide(template_svcs.TemplateService),
        "template_schema": starlite.Provide(database_deps.get_template_schema),
    }

    @starlite.post()
    async def add_certificate_template(
        self,
        database: crud.DatabaseImpl,
        imagekit_client: imagekit.ImageKitClient,
        template_service: template_svcs.TemplateService,
        template_schema: type[templates.Templates],
        data: dict[
            str, datastructures.UploadFile | list[datastructures.UploadFile]
        ] = starlite.Body(media_type=starlite.RequestEncodingType.MULTI_PART),
    ) -> typing.Any:
        return await template_service.add_certificate_template(
            data=data,
            database=database,
            imagekit_client=imagekit_client,
            template_schema=template_schema,
        )

    @starlite.get()
    async def list_certificate_templates(self) -> typing.Any:
        return {}
