import typing

import starlite

from app.api.api_v1.dependencies import database
from app.api.api_v1.routes.services import configuration as service


class TemplateController(starlite.Controller):
    path = "/templates"

    dependencies: typing.Optional[dict[str, "starlite.Provide"]] = {
        "certificate_service": starlite.Provide(service.ConfigurationService),
        "database": starlite.Provide(database.get_db_impl),
    }

    @starlite.get()
    async def list_templates(self) -> typing.Any:
        return {}
