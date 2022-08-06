import pydantic
from nacl.bindings import crypto_core
from solana import publickey

from app.core import exceptions
from app.models.domain import app_model


class SolanaUser(app_model.AppModel):
    wallet_address: str

    @pydantic.validator("wallet_address")
    def wallet_address_must_be_on_curve(cls, wallet_address: str) -> str:
        valid_point = crypto_core.crypto_core_ed25519_is_valid_point(
            bytes(publickey.PublicKey(wallet_address))
        )

        if not valid_point:
            raise exceptions.OnCurveException("the point must be on the curve")

        return wallet_address
