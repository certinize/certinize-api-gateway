import starlite

from app.models import domain


class UserController(starlite.Controller):
    path = "/users"

    @starlite.post(path="/auth")
    async def auth(
        self,
        data: domain.SolanaUser = starlite.Body(
            media_type=starlite.RequestEncodingType.JSON
        ),
    ) -> domain.SolanaUser:
        """Authenticate and authorize Solana user.

        Args:
            wallet_address (domain.SolanaUser): _description_

        Returns:
            domain.SolanaUser: _description_
        """
        return data
