import typing

import starlite

from app.api.api_v1.dependencies import database
from app.api.api_v1.routes.services import configuration as service


class CertificateController(starlite.Controller):
    path = "/certificates"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "certificate_service": starlite.Provide(service.ConfigurationService),
        "database": starlite.Provide(database.get_db_impl),
    }

    @starlite.post()
    async def generate_certificate(self, data: typing.Any) -> typing.Any:
        return data
