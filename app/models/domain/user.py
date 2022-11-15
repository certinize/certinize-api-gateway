import pydantic

from app import utils
from app.models.domain import app_model


class UserUpdate(app_model.AppModel):
    name: str | None = pydantic.Field(default=None)
    api_key: pydantic.UUID5 | None = pydantic.Field(default=None)
    website: pydantic.HttpUrl | None = pydantic.Field(default=None)
    user_avatar: str | None = pydantic.Field(default=None)

    @pydantic.validator("user_avatar")
    @classmethod
    def organization_logo_is_valid_base64(cls, value: str):
        return utils.image_is_valid_base64(value)


class UnverifiedUser(app_model.AppModel):
    pubkey: str
    pvtkey: str
    info_link: pydantic.HttpUrl
    official_website: pydantic.HttpUrl
    official_email: pydantic.EmailStr
    organization_name: str
    organization_logo: str
    organization_id: str = pydantic.Field(min_length=1)

    @pydantic.validator("pubkey")
    @classmethod
    def recipient_pubkey_on_curve(cls, value: str):
        return utils.pubkey_on_curve(value)

    @pydantic.validator("pvtkey")
    @classmethod
    def recipient_pvtkey_on_curve(cls, value: str):
        return utils.pvtkey_on_curve(value)

    @pydantic.validator("organization_id")
    @classmethod
    def organization_id_is_valid_base64(cls, value: str):
        return utils.image_is_valid_base64(value)

    @pydantic.validator("organization_logo")
    @classmethod
    def organization_logo_is_valid_base64(cls, value: str):
        return utils.image_is_valid_base64(value)
