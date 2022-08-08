import typing

import starlite

from app.api.api_v1.dependencies import database
from app.api.api_v1.routes.services import configuration as service


class IssuanceController(starlite.Controller):
    path = "/certificates"

    dependencies: typing.Optional[dict[str, "starlite.Provide"]] = {
        "certificate_service": starlite.Provide(service.ConfigurationService),
        "database": starlite.Provide(database.get_db_impl),
    }

    @starlite.post()
    async def transfer_certificate(self, data: typing.Any) -> typing.Any:
        return data
