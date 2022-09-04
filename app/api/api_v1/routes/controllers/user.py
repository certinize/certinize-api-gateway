import starlite

from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.routes.services import user
from app.db import crud
from app.models.schemas import users


class UserController(starlite.Controller):
    path = "/users"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "user_service": starlite.Provide(user.UserService),
        "database": starlite.Provide(database_deps.get_db_impl),
        "solana_user_schema": starlite.Provide(database_deps.get_solana_users_schema),
    }

    @starlite.get(path="/{wallet_address:str}")
    async def auth_solana_user(
        self,
        user_service: user.UserService,
        solana_user_schema: type[users.SolanaUsers],
        database: crud.DatabaseImpl,
        wallet_address: str = starlite.Parameter(
            title="Auth Solana User",
            description="Authenticate and authorize solana user and provide API key",
        ),
    ) -> users.SolanaUsers | starlite.ValidationException:
        solana_user = await user_service.auth(
            wallet_address, solana_user_schema, database
        )

        return solana_user

    @starlite.patch()
    async def update_solana_user(
        self, solana_user_schema: type[users.SolanaUsers]
    ) -> None:
        ...
