import pydantic
import sqlmodel
from sqlalchemy import orm


class SolanaUsers(sqlmodel.SQLModel, table=True):
    wallet_address: str | None = sqlmodel.Field(  # type: ignore
        default=None, primary_key=True
    )
    api_key: pydantic.UUID5
    name: str | None
    website: pydantic.HttpUrl | None

    @classmethod
    @orm.declared_attr
    def __tablename__(cls):
        return "solana_users"
