# flake8: noqa
# pylint: disable=R0903

import typing

import pydantic
import sqlmodel


class TemplateConfigurations(sqlmodel.SQLModel, table=True):
    template_config_id: pydantic.UUID1 | None = sqlmodel.Field(  # type: ignore
        default=None, primary_key=True
    )
    template_config_name: str
    config_meta: dict[str, typing.Any] = sqlmodel.Field(  # type: ignore
        default={}, sa_column=sqlmodel.Column(sqlmodel.JSON)
    )

    class Config(sqlmodel.SQLModel.Config):
        arbitrary_types_allowed = True
