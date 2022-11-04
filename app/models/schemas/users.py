import pydantic
import sqlmodel
from sqlalchemy import orm


class SolanaUsers(sqlmodel.SQLModel, table=True):
    pubkey: str | None = sqlmodel.Field(default=None, primary_key=True)  # type: ignore
    api_key: pydantic.UUID5 | None = sqlmodel.Field(default=None)  # type: ignore
    name: str | None = sqlmodel.Field(default=None)  # type: ignore
    website: pydantic.HttpUrl | None = sqlmodel.Field(default=None)  # type: ignore
    user_avatar: str | None = sqlmodel.Field(default=None)  # type: ignore

    @classmethod
    @orm.declared_attr
    def __tablename__(cls):
        return "solana_users"


class VerificationRequests(sqlmodel.SQLModel, table=True):
    pubkey: str | None = sqlmodel.Field(default=None, primary_key=True)  # type: ignore
    info_link: pydantic.HttpUrl
    official_website: pydantic.HttpUrl
    official_email: pydantic.EmailStr
    organization_id: str
    approved: bool = sqlmodel.Field(default=False)  # type: ignore
    verified_on: str | None = sqlmodel.Field(default=None)  # type: ignore

    @classmethod
    @orm.declared_attr
    def __tablename__(cls):
        return "verification_requests"
