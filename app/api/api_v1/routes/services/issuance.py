# pylint: disable=R0903
import typing

from app.models.domain import issuance
from app.services import blockchain_api


class IssuanceService:
    @staticmethod
    async def transfer_certificate(
        data: issuance.IssuanceRequest,
        blockchain_api: blockchain_api.BlockchainInterface,
    ) -> tuple[typing.Any, int]:
        issue_req = data.with_fields(callback_endpoint=(str, ...))

        return await blockchain_api.issue_certificate(
            issue_req(
                callback_endpoint="http://localhost:8000/api/v1/issuances/callback",
                issuer_meta=data.issuer_meta,
                recipient_meta=data.recipient_meta,
            )
        )
