import enum
import re

import pydantic
import solders.keypair as solders_keypair  # type: ignore # pylint: disable=E0401
from nacl.bindings import crypto_core
from solana import publickey

from app.models.domain import app_model

PanicException = re.compile(r"\((.*?)\)")
InvalidCharacter = re.compile(r"(?<=: ).*(?=\s{)")


class RustError(enum.Enum):
    InvalidCharacter = "found unsupported characters"


def raise_rust_error(error: BaseException) -> None:
    try:
        raise ValueError(PanicException.findall(str(error))[1]) from error
    except IndexError:
        raise ValueError(
            RustError[InvalidCharacter.findall(str(error))[0]].value
        ) from error


class IssuerMeta(app_model.AppModel):
    issuer_id: pydantic.UUID1
    issuer_pubkey: str
    issuer_pvtket: str
    issuer_name: str | None = None
    issuer_email: pydantic.EmailStr | None = None
    issuer_website: pydantic.HttpUrl | None = None

    @pydantic.validator("issuer_pubkey")
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

    @pydantic.validator("issuer_pvtket")
    @classmethod
    def recipient_pvtkey_on_curve(cls, value: str):
        try:
            solders_keypair.Keypair().from_base58_string(value)
        except BaseException as base_err:
            raise_rust_error(base_err)

        return value


class RecipientMeta(app_model.AppModel):
    recipient_email: pydantic.EmailStr
    recipient_name: str
    recipient_pubkey: str
    recipient_ecert_url: pydantic.HttpUrl

    @pydantic.validator("recipient_pubkey")
    @classmethod
    def issuer_pubkey_on_curve(cls, value: str):
        try:
            crypto_core.crypto_core_ed25519_is_valid_point(
                bytes(publickey.PublicKey(value))
            )
        except ValueError as val_err:
            val_err.args = ("the point must be on the curve",)
            raise val_err from val_err

        return value


class IssuanceRequest(app_model.AppModel):
    issuer_meta: IssuerMeta
    recipient_meta: list[RecipientMeta]
