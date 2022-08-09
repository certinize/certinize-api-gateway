import typing

import pydantic
import sqlmodel


class SolanaUsers(sqlmodel.SQLModel, table=True):
    user_id: typing.Optional[pydantic.UUID1] = sqlmodel.Field(default=None, primary_key=True)  # type: ignore
    wallet_address: str
    api_key: pydantic.UUID5
