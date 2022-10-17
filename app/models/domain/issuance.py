import enum
import re

import pydantic
import solders.keypair as solders_keypair  # type: ignore # pylint: disable=E0401

from app import utils
from app.models.domain import app_model

PANIC_EXC = re.compile(r"\((.*?)\)")
INVALID_CHAR = re.compile(r"(?<=: ).*(?=\s{)")


class RustError(enum.Enum):
    INVALIDCHARACTER = "found unsupported characters"


def raise_rust_error(error: BaseException) -> None:
    try:
        raise ValueError(PANIC_EXC.findall(str(error))[1]) from error
    except IndexError:
        raise ValueError(
            RustError[INVALID_CHAR.findall(str(error))[0].upper()].value
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
        return utils.pubkey_on_curve(value)

    @pydantic.validator("issuer_pvtket")
    @classmethod
    def recipient_pvtkey_on_curve(cls, value: str):
        try:
            solders_keypair.Keypair().from_base58_string(value)
        except BaseException as base_err:  # pylint: disable=W0703
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
        return utils.pubkey_on_curve(value)


class IssuanceRequest(app_model.AppModel):
    issuer_meta: IssuerMeta
    recipient_meta: list[RecipientMeta]
