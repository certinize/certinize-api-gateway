import typing

# import pydantic
import starlite

from app.api.api_v1.dependencies import associated_services
from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.routes.services import issuance as service
from app.models.domain import issuance
from app.services import blockchain_api


class IssuanceController(starlite.Controller):
    path = "/issuances"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "engine": starlite.Provide(database_deps.get_db_engine),
        "issuance_service": starlite.Provide(service.IssuanceService),
        "blockchain_api": starlite.Provide(
            associated_services.get_blockchain_api_client
        ),
    }

    @starlite.post()
    async def transfer_certificate(
        self,
        data: issuance.IssuanceRequest,
        issuance_service: service.IssuanceService,
        blockchain_api_: blockchain_api.BlockchainInterface,
    ) -> starlite.Response[typing.Any | None]:
        result = await issuance_service.transfer_certificate(data, blockchain_api_)

        return starlite.Response(
            content=result[0],
            status_code=result[0].get("code") or result[1],
            media_type="application/json",
        )
