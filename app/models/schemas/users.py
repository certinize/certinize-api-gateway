import typing

import pydantic
import sqlmodel


class SolanaUser(sqlmodel.SQLModel, table=True):
    id: typing.Optional[str] = sqlmodel.Field(default=None, primary_key=True)  # type: ignore
    wallet_address: str
    api_key: pydantic.UUID4
