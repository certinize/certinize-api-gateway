import uuid

import starlite
from sqlalchemy import exc

from app import utils
from app.core import exceptions
from app.db import crud
from app.models.schemas import users


class UserService:
    async def auth(
        self,
        wallet_address: str,
        solana_user_schema: type[users.SolanaUsers],
        database: crud.DatabaseImpl,
        utils: utils.Utils,
    ) -> users.SolanaUsers:

        try:
            wallet_address = await utils.wallet_address_must_be_on_curve(
                wallet_address=wallet_address
            )
        except (ValueError, exceptions.OnCurveException) as err:
            raise starlite.ValidationException(str(err)) from err

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
            schema = solana_user_schema(
                user_id=user_id, wallet_address=wallet_address, api_key=api_key
            )

            await database.add_row(schema)

            return schema
