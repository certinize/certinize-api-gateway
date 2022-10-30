import pydantic
import sqlmodel
from sqlalchemy import orm


class SolanaUsers(sqlmodel.SQLModel, table=True):
    wallet_address: str | None = sqlmodel.Field(  # type: ignore
        default=None, primary_key=True
    )
    api_key: pydantic.UUID5

    @classmethod
    @orm.declared_attr
    def __tablename__(cls):
        return "solana_users"


class VerificationRequests(sqlmodel.SQLModel, table=True):
    pubkey: str | None = sqlmodel.Field(default=None, primary_key=True)  # type: ignore
    organization_name: str
    organization_logo: str
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
