import pydantic
import sqlmodel
from sqlalchemy import orm


class SolanaUsers(sqlmodel.SQLModel, table=True):
    user_id: pydantic.UUID1 | None = sqlmodel.Field(  # type: ignore
        default=None, primary_key=True
    )
    wallet_address: str
    api_key: pydantic.UUID5

    @orm.declared_attr
    def __tablename__(cls):
        return "solana_users"
