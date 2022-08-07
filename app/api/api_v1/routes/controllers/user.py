import typing

import starlite

from app.api.api_v1.dependencies import database, response
from app.api.api_v1.routes.services import user
from app.db import crud
from app.models import domain
from app.models.schemas import users


class UserController(starlite.Controller):
    path = "/users"

    dependencies: typing.Optional[dict[str, "starlite.Provide"]] = {
        "user_service": starlite.Provide(user.UserService),
        "database": starlite.Provide(database.get_db_impl),
    }

    @starlite.post(
        path="/auth",
        dependencies={
            "solana_user_schema": starlite.Provide(database.get_solana_user_schema)
        },
    )
    async def auth(
        self,
        data: domain.SolanaUser,
        user_service: user.UserService,
        solana_user_schema: type[users.SolanaUser],
        database: crud.DatabaseImpl,
    ) -> response.AuthResponse:
        solana_user = await user_service.auth(
            data.wallet_address, solana_user_schema, database
        )

        return solana_user
