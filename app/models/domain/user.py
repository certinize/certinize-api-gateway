import pydantic
import sqlmodel

from app import utils
from app.models.domain import app_model


class UserUpdate(app_model.AppModel):
    name: str | None = sqlmodel.Field(default=None)  # type: ignore
    api_key: pydantic.UUID5 | None = sqlmodel.Field(default=None)  # type: ignore
    website: pydantic.HttpUrl | None = sqlmodel.Field(default=None)  # type: ignore
    user_avatar: str | None = sqlmodel.Field(default=None)  # type: ignore

    @pydantic.validator("user_avatar")
    @classmethod
    def organization_logo_is_valid_base64(cls, value: str):
        return utils.image_is_valid_base64(value)


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
