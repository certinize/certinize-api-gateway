# pylint: disable=R0903
import typing

import starlite

from app.db import crud
from app.models.domain import issuance
from app.models.schemas import users
from app.services import blockchain_api


class IssuanceService:
    @staticmethod
    async def get_unsigned_msg(
        database: crud.DatabaseImpl,
        public_key: str,
        blockchain_api_: blockchain_api.BlockchainInterface,
    ) -> dict[str, str]:
        user = await database.select(users.SolanaUsers(), "pubkey", public_key)
        pvtkey = user.one().pvtkey

        if pvtkey is None:
            raise starlite.HTTPException(
                status_code=400,
                detail="User is not verified",
            )

        return await blockchain_api_.get_unsigned_msg(
            {"pubkey": public_key, "pvtkey": pvtkey}
        )

    @staticmethod
    async def transfer_certificate(
        data: issuance.IssuanceRequest,
        blockchain_api_: blockchain_api.BlockchainInterface,
    ) -> tuple[typing.Any, int]:
        return await blockchain_api_.issue_certificate(data)
