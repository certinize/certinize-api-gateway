import typing
import uuid

import pydantic
import starlite
from nacl.bindings import crypto_core
from solana import publickey
from sqlalchemy import exc

from app.core import exceptions
from app.db import crud
from app.models.domain import user as user_domain
from app.models.schemas import users


class UserService:
    async def _fetch_user(
        self,
        database: crud.DatabaseImpl,
        wallet_address: str,
        solana_user_schema: type[users.SolanaUsers],
    ):
        user: dict[str, typing.Any] = {}

        try:
            solana_user = await database.select_row(
                solana_user_schema(
                    wallet_address=wallet_address,
                    api_key=uuid.uuid1(),
                ),
                "wallet_address",
                wallet_address,
            )

            user = solana_user.one().dict() | user
        except exc.NoResultFound:
            api_key = uuid.uuid5(uuid.uuid4(), wallet_address)
            schema = solana_user_schema(
                wallet_address=wallet_address,
                api_key=api_key,
            )
            result = schema.copy()

            await database.add_row(schema)

            user = result.dict() | user

        return user

    async def _fetch_verification(
        self, database: crud.DatabaseImpl, wallet_address: str
    ) -> dict[str, typing.Any]:
        verification: dict[str, typing.Any] = {}

        try:
            vequest = await database.select_row(
                users.VerificationRequests(
                    pubkey=wallet_address,
                    organization_name="",
                    organization_logo="",
                    info_link=pydantic.HttpUrl("", scheme=""),
                    official_website=pydantic.HttpUrl("", scheme=""),
                    official_email=pydantic.EmailStr(""),
                    organization_id="",
                    approved=False,
                ),
                "pubkey",
                wallet_address,
            )
            verification = vequest.one()
        except exc.NoResultFound:
            verification = {}

        return verification

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
    ) -> dict[str, typing.Any]:
        try:
            wallet_address = await self.wallet_address_must_be_on_curve(
                wallet_address=wallet_address
            )
        except (ValueError, exceptions.OnCurveException) as err:
            raise starlite.ValidationException(str(err)) from err

        return {
            "user": await self._fetch_user(
                database=database,
                wallet_address=wallet_address,
                solana_user_schema=solana_user_schema,
            ),
            "verification": await self._fetch_verification(database, wallet_address),
        }

    async def verify_user(
        self,
        data: user_domain.UnverifiedUser,
        database: crud.DatabaseImpl,
        vequest_schema: type[users.VerificationRequests],
    ) -> users.VerificationRequests:
        schema = vequest_schema(
            pubkey=data.pubkey,
            organization_name=data.organization_name,
            organization_logo=data.organization_logo,
            info_link=data.info_link,
            official_website=data.official_website,
            official_email=data.official_email,
            organization_id=data.organization_id,
        )
        result = schema.copy()

        try:
            await database.add_row(schema)
        except exc.IntegrityError as err:
            raise starlite.ValidationException(
                f"{data.pubkey} already sent a verification request", status_code=409
            ) from err

        return result
