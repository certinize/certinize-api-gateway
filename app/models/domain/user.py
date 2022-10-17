import base64
import binascii

import pydantic

from app import utils
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
        return utils.pubkey_on_curve(value)

    @pydantic.validator("organization_id")
    @classmethod
    def image_is_valid_base64(cls, value: str):
        try:
            base64.b64decode(value)
        except binascii.Error as error:
            raise ValueError("image is not a valid base64 string") from error

        return value
