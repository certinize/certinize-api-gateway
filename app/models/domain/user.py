import pydantic

from app import utils
from app.models.domain import app_model


class SolanaUser(app_model.AppModel):
    pubkey: str
    pvtkey: str


class UnverifiedUser(app_model.AppModel):
    pubkey: str
    organization_name: str
    organization_logo: str
    info_link: pydantic.HttpUrl
    official_website: pydantic.HttpUrl
    official_email: pydantic.EmailStr
    organization_id: str

    @pydantic.validator("pubkey")
    @classmethod
    def recipient_pubkey_on_curve(cls, value: str):
        return utils.pubkey_on_curve(value)

    @pydantic.validator("organization_id")
    @classmethod
    def organization_id_is_valid_base64(cls, value: str):
        return utils.image_is_valid_base64(value)

    @pydantic.validator("organization_logo")
    @classmethod
    def organization_logo_is_valid_base64(cls, value: str):
        return utils.image_is_valid_base64(value)
