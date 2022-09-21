import pydantic

from app.models.domain import app_model


class SolanaUser(app_model.AppModel):
    pubkey: str
    pvtkey: str


class UnverifiedUser(app_model.AppModel):
    pubkey: str
    pvtkey: str
    email: pydantic.EmailStr
    website: pydantic.HttpUrl
    address: str
