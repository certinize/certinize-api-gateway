import base64
import binascii

import pydantic
from nacl.bindings import crypto_core
from solana import publickey

from app.models.domain import app_model


class SolanaUser(app_model.AppModel):
    pubkey: str
    pvtkey: str


class UnverifiedUser(app_model.AppModel):
    pubkey: str
    info_link: pydantic.HttpUrl
    official_website: pydantic.HttpUrl
    official_email: pydantic.EmailStr
    organization_id: str

    @pydantic.validator("pubkey")
    @classmethod
    def recipient_pubkey_on_curve(cls, value: str):
        try:
            crypto_core.crypto_core_ed25519_is_valid_point(
                bytes(publickey.PublicKey(value))
            )
        except ValueError as val_err:
            val_err.args = ("the point must be on the curve",)
            raise val_err from val_err

        return value

    @pydantic.validator("organization_id")
    @classmethod
    def image_is_valid_base64(cls, value: str):
        try:
            base64.b64decode(value)
        except binascii.Error as error:
            raise ValueError(f"image is not a valid base64 string") from error

        return value
