import typing

import pydantic
import starlite

from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.routes.services import issuance as service


class IssuanceController(starlite.Controller):
    path = "/issuances"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "engine": starlite.Provide(database_deps.get_db_engine),
        "issuance_service": starlite.Provide(service.IssuanceService),
    }

    @starlite.get(path="/{certificate_collection_id:uuid}")
    async def transfer_certificate(
        self, certificate_collection_id: pydantic.UUID1
    ) -> typing.Any:
        return certificate_collection_id
