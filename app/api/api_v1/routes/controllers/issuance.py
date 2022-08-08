import typing

import starlite
import pydantic
from app.api.api_v1.dependencies import database
from app.api.api_v1.routes.services import configuration as service


class IssuanceController(starlite.Controller):
    path = "/issuances"

    dependencies: typing.Optional[dict[str, "starlite.Provide"]] = {
        "certificate_service": starlite.Provide(service.ConfigurationService),
        "database": starlite.Provide(database.get_db_impl),
    }

    @starlite.post(path="/{certificate_collection_id:uuid}")
    async def transfer_certificate(
        self, certificate_collection_id: pydantic.UUID1
    ) -> typing.Any:
        return certificate_collection_id
