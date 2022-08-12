import pydantic
import sqlmodel


class SolanaUsers(sqlmodel.SQLModel, table=True):
    user_id: pydantic.UUID1 | None = sqlmodel.Field(  # type: ignore
        default=None, primary_key=True
    )
    wallet_address: str
    api_key: pydantic.UUID5
