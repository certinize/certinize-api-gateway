import typing

import pydantic
import starlite

from app.api.api_v1.dependencies import database
from app.api.api_v1.routes.services import configuration as service


class IssuanceController(starlite.Controller):
    path = "/issuances"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "certificate_service": starlite.Provide(service.ConfigurationService),
        "database": starlite.Provide(database.get_db_impl),
    }

    @starlite.post(path="/{certificate_collection_id:uuid}")
    async def transfer_certificate(
        self, certificate_collection_id: pydantic.UUID1
    ) -> typing.Any:
        return certificate_collection_id
