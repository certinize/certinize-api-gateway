import typing

import starlite

from app.api.api_v1.dependencies import database, schema
from app.api.api_v1.routes.services import user
from app.db import crud
from app.models import domain
from app.models.schemas import users


class UserController(starlite.Controller):
    path = "/users"

    dependencies: typing.Optional[dict[str, "starlite.Provide"]] = {
        "user_service": starlite.Provide(user.UserService),
        "solana_user_schema": starlite.Provide(schema.get_solana_user_schema),
        "database": starlite.Provide(database.get_db_impl),
    }

    @starlite.post(path="/auth")
    async def auth(
        self,
        user_service: user.UserService,
        solana_user_schema: type[users.SolanaUser],
        database: crud.DatabaseImpl,
        data: domain.SolanaUser,
    ) -> typing.Any:
        solana_user = await user_service.auth(
            data.wallet_address, solana_user_schema, database
        )

        return solana_user
