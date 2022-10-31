import pydantic

from app import utils
from app.models.domain import app_model


class IssuerMeta(app_model.AppModel):
    issuer_pubkey: str
    issuer_name: str | None = None
    issuer_email: pydantic.EmailStr | None = None
    issuer_website: pydantic.HttpUrl | None = None

    @pydantic.validator("issuer_pubkey")
    @classmethod
    def recipient_pubkey_on_curve(cls, value: str):
        return utils.pubkey_on_curve(value)


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
    signature: str
    issuer_meta: IssuerMeta
    recipient_meta: list[RecipientMeta]
