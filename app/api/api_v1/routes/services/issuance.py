# pylint: disable=R0903
import typing

from app.models.domain import issuance
from app.services import blockchain_api


class IssuanceService:
    @staticmethod
    async def get_unsigned_msg(
        public_key: str, blockchain_api_: blockchain_api.BlockchainInterface
    ) -> dict[str, str]:
        return await blockchain_api_.get_unsigned_msg(public_key)

    @staticmethod
    async def transfer_certificate(
        data: issuance.IssuanceRequest,
        blockchain_api_: blockchain_api.BlockchainInterface,
    ) -> tuple[typing.Any, int]:
        return await blockchain_api_.issue_certificate(data)
