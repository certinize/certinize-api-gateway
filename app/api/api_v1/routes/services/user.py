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
        pubkey: str,
        solana_user_schema: type[users.SolanaUsers],
    ):
        user: dict[str, typing.Any] = {}

        try:
            solana_user = await database.select(
                solana_user_schema(
                    pubkey=pubkey,
                    api_key=uuid.uuid1(),
                ),
                "pubkey",
                pubkey,
            )

            user = solana_user.one().dict() | user
        except exc.NoResultFound:
            api_key = uuid.uuid5(uuid.uuid4(), pubkey)
            schema = solana_user_schema(
                pubkey=pubkey,
                api_key=api_key,
            )
            result = schema.copy()

            await database.add(schema)

            user = result.dict() | user

        return user

    async def _fetch_verification(
        self, database: crud.DatabaseImpl, pubkey: str
    ) -> dict[str, typing.Any]:
        verification: dict[str, typing.Any] = {}

        try:
            vequest = await database.select(
                users.VerificationRequests(
                    pubkey=pubkey,
                    info_link=pydantic.HttpUrl("", scheme=""),
                    official_website=pydantic.HttpUrl("", scheme=""),
                    official_email=pydantic.EmailStr(""),
                    organization_id="",
                    approved=False,
                ),
                "pubkey",
                pubkey,
            )
            verification = vequest.one()
        except exc.NoResultFound:
            verification = {}

        return verification

    async def pubkey_must_be_on_curve(self, pubkey: str) -> str:
        try:
            valid_point = crypto_core.crypto_core_ed25519_is_valid_point(
                bytes(publickey.PublicKey(pubkey))
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

        return pubkey

    async def auth(
        self,
        pubkey: str,
        database: crud.DatabaseImpl,
    ) -> dict[str, typing.Any]:
        try:
            pubkey = await self.pubkey_must_be_on_curve(pubkey=pubkey)
        except (ValueError, exceptions.OnCurveException) as err:
            raise starlite.ValidationException(str(err)) from err

        return {
            "user": await self._fetch_user(
                database=database,
                pubkey=pubkey,
                solana_user_schema=users.SolanaUsers,
            ),
            "verification": await self._fetch_verification(database, pubkey),
        }

    async def verify_user(
        self,
        data: user_domain.UnverifiedUser,
        database: crud.DatabaseImpl,
        token: str,
    ) -> users.VerificationRequests:
        vequest = users.VerificationRequests(
            pubkey=data.pubkey,
            info_link=data.info_link,
            official_website=data.official_website,
            official_email=data.official_email,
            organization_id=data.organization_id,
        )
        vequest_ = vequest.copy()

        try:
            await database.add(vequest)
            await database.update(
                users.SolanaUsers(
                    pubkey=data.pubkey,
                    pvtkey=data.pvtkey,
                    api_key=uuid.UUID(token),
                    name=data.organization_name,
                    website=data.official_website,
                    email=data.official_email,
                ),
                "pubkey",
            )
        except exc.IntegrityError as err:
            raise starlite.ValidationException(
                f"User already sent a verification request: {data.pubkey}",
                status_code=409,
            ) from err

        return vequest_

    async def update_user(
        self,
        data: user_domain.UserUpdate,
        database: crud.DatabaseImpl,
        solana_user_schema: type[users.SolanaUsers],
        pubkey: str,
    ) -> users.SolanaUsers:
        schema = solana_user_schema(
            pubkey=pubkey,
            name=data.name,
            website=data.website,
            user_avatar=data.user_avatar,
        )

        try:
            await database.update(schema, "pubkey")
        except exc.IntegrityError as err:
            raise starlite.ValidationException(
                str(err),
                status_code=409,
            ) from err
        except exc.NoResultFound as err:
            raise starlite.ValidationException(
                f"{pubkey} does not exist", status_code=404
            ) from err

        return schema

    async def get_verification(
        self,
        database: crud.DatabaseImpl,
        pubkey: str,
    ) -> dict[str, typing.Any]:
        try:
            vequest = await database.select(
                users.VerificationRequests(
                    pubkey=pubkey,
                    info_link=pydantic.HttpUrl("", scheme=""),
                    official_website=pydantic.HttpUrl("", scheme=""),
                    official_email=pydantic.EmailStr(""),
                    organization_id="",
                    approved=False,
                ),
                "pubkey",
                pubkey,
            )
            user = await self._fetch_user(
                database=database,
                pubkey=pubkey,
                solana_user_schema=users.SolanaUsers,
            )
            verif = vequest.one().dict()
            verif["name"] = user["name"]

            del verif["info_link"]
            del verif["organization_id"]

            return verif
        except exc.NoResultFound as err:
            raise starlite.ValidationException(
                f"{pubkey} does not exist", status_code=404
            ) from err
