import typing

import starlite
from starlette import datastructures

from app.api.api_v1.dependencies import database
from app.api.api_v1.routes.services import configuration as service


class TemplateController(starlite.Controller):
    path = "/templates"

    dependencies: typing.Optional[dict[str, "starlite.Provide"]] = {
        "certificate_service": starlite.Provide(service.ConfigurationService),
        "database": starlite.Provide(database.get_db_impl),
    }

    @starlite.post()
    async def add_certificate_template(
        self,
        data: dict[str, datastructures.UploadFile] = starlite.Body(
            media_type=starlite.RequestEncodingType.MULTI_PART
        ),
    ) -> None:
        return

    @starlite.get()
    async def list_certificate_templates(self) -> typing.Any:
        return {}
