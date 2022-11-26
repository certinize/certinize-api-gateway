import typing

import starlite

from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.routes.services import user as user_service
from app.db import crud
from app.models.domain import user as user_domain
from app.models.schemas import users


class UserController(starlite.Controller):
    path = "/users"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "user_service_": starlite.Provide(user_service.UserService),
        "database": starlite.Provide(database_deps.get_db_impl),
    }

    @starlite.get(path="/{public_key:str}")
    async def auth_user(
        self,
        user_service_: user_service.UserService,
        database: crud.DatabaseImpl,
        public_key: str = starlite.Parameter(
            title="Auth Solana User",
            description="Authenticate and authorize solana user and provide API key",
        ),
    ) -> dict[str, typing.Any] | starlite.ValidationException:
        return await user_service_.auth(public_key, database)

    @starlite.post()
    async def verify_user(
        self,
        data: user_domain.UnverifiedUser,
        database: crud.DatabaseImpl,
        user_service_: user_service.UserService,
        token: str = starlite.Parameter(header="X-API-KEY", min_length=36),
    ) -> users.VerificationRequests | starlite.ValidationException:
        return await user_service_.verify_user(data, database, token)

    @starlite.patch(path="/{public_key:str}")
    async def update_user(  # pylint: disable=R0913
        self,
        data: user_domain.UserUpdate,
        database: crud.DatabaseImpl,
        user_service_: user_service.UserService,
        public_key: str = starlite.Parameter(
            title="Update Solana User",
            description="Update solana user",
        ),
        token: str = starlite.Parameter(header="X-API-KEY", min_length=36),
    ) -> users.SolanaUsers | starlite.ValidationException:
        _ = token
        return await user_service_.update_user(
            data, database, users.SolanaUsers, public_key
        )

    @starlite.get(path="/verification/{public_key:str}")
    async def get_verification(
        self,
        database: crud.DatabaseImpl,
        user_service_: user_service.UserService,
        public_key: str = starlite.Parameter(),
    ) -> dict[str, typing.Any]:
        return await user_service_.get_verification(database, public_key)
