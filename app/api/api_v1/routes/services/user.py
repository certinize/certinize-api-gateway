import typing
import uuid

from sqlalchemy import exc

from app.db import crud
from app.models.schemas import users


class UserService:
    async def auth(
        self,
        wallet_address: str,
        solana_user_schema: type[users.SolanaUser],
        database: crud.DatabaseImpl,
    ) -> typing.Any:
        try:
            solana_user = await database.select_row(
                solana_user_schema(wallet_address=wallet_address, api_key=uuid.uuid1()),
                "wallet_address",
                wallet_address,
            )
            return solana_user.one()
        except exc.NoResultFound:
            user_id = uuid.uuid1()
            api_key = uuid.uuid5(uuid.uuid4(), wallet_address)
            await database.add_row(
                solana_user_schema(
                    user_id=user_id, wallet_address=wallet_address, api_key=api_key
                )
            )
            return {
                "wallet_address": wallet_address,
                "api_key": api_key,
                "id": id,
            }
