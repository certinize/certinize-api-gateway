import typing

import starlite

from app import utils
from app.api.api_v1.dependencies import database
from app.api.api_v1.routes.services import user
from app.db import crud
from app.models.schemas import users


class UserController(starlite.Controller):
    path = "/users"

    dependencies: typing.Optional[dict[str, "starlite.Provide"]] = {
        "user_service": starlite.Provide(user.UserService),
        "database": starlite.Provide(database.get_db_impl),
        "utils": starlite.Provide(utils.Utils),
    }

    @starlite.get(
        path="/{wallet_address:str}",
        dependencies={
            "solana_user_schema": starlite.Provide(database.get_solana_user_schema)
        },
    )
    async def auth_solana_user(
        self,
        user_service: user.UserService,
        solana_user_schema: type[users.SolanaUsers],
        database: crud.DatabaseImpl,
        utils: utils.Utils,
        wallet_address: str = starlite.Parameter(
            title="Auth Solana User",
            description="Authenticate and authorize solana user and provide API key",
        ),
    ) -> users.SolanaUsers | starlite.ValidationException:
        solana_user = await user_service.auth(
            wallet_address, solana_user_schema, database, utils
        )

        return solana_user
