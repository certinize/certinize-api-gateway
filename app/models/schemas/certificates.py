import typing

import pydantic
import sqlmodel


class CertificateConfiguration(sqlmodel.SQLModel, table=True):
    template_config_id: typing.Optional[pydantic.UUID1] = sqlmodel.Field(default=None, primary_key=True)  # type: ignore
    template_config_name: str
    config_meta: dict[str, typing.Any] = sqlmodel.Field(default={}, sa_column=sqlmodel.Column(sqlmodel.JSON))  # type: ignore

    class Config:  # type: ignore
        arbitrary_types_allowed = True
