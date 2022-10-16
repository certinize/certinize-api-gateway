import uuid

import starlite
from nacl.bindings import crypto_core
from solana import publickey
from sqlalchemy import exc

from app.core import exceptions
from app.db import crud
from app.models.domain import user as user_domain
from app.models.schemas import users


class UserService:  # pylint: disable=R0903
    async def wallet_address_must_be_on_curve(self, wallet_address: str) -> str:
        try:
            valid_point = crypto_core.crypto_core_ed25519_is_valid_point(
                bytes(publickey.PublicKey(wallet_address))
            )
        except ValueError as val_err:
            err = (
                str(val_err)
                .replace("'", "")
                .replace("(", "")
                .replace(")", "")
                .replace(",", "")
            )
            raise ValueError(err) from val_err

        if not valid_point:
            raise exceptions.OnCurveException("the point must be on the curve")

        return wallet_address

    async def auth(
        self,
        wallet_address: str,
        solana_user_schema: type[users.SolanaUsers],
        database: crud.DatabaseImpl,
    ) -> users.SolanaUsers:
        try:
            wallet_address = await self.wallet_address_must_be_on_curve(
                wallet_address=wallet_address
            )
        except (ValueError, exceptions.OnCurveException) as err:
            raise starlite.ValidationException(str(err)) from err

        try:
            solana_user = await database.select_row(
                solana_user_schema(
                    wallet_address=wallet_address,
                    api_key=uuid.uuid1(),
                    name=None,
                    website=None,
                ),
                "wallet_address",
                wallet_address,
            )
            return solana_user.one()
        except exc.NoResultFound:
            api_key = uuid.uuid5(uuid.uuid4(), wallet_address)
            schema = solana_user_schema(
                wallet_address=wallet_address,
                api_key=api_key,
                name=None,
                website=None,
            )
            result = schema.copy()

            await database.add_row(schema)

            return result

    async def verify_user(
        self,
        data: user_domain.UnverifiedUser,
        database: crud.DatabaseImpl,
        vequest_schema: type[users.VerificationRequests],
    ) -> users.VerificationRequests:
        schema = vequest_schema(
            pubkey=data.pubkey,
            info_link=data.info_link,
            official_website=data.official_website,
            official_email=data.official_email,
            organization_id=data.organization_id,
        )
        result = schema.copy()

        try:
            await database.add_row(schema)
        except exc.IntegrityError as err:
            raise starlite.ValidationException(str(err), status_code=409) from err

        return result
