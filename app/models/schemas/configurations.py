# flake8: noqa
# pylint: disable=R0903

import typing

import pydantic
import sqlmodel
from sqlalchemy import orm


class Configurations(sqlmodel.SQLModel, table=True):
    template_config_id: pydantic.UUID1 | None = sqlmodel.Field(  # type: ignore
        default=None, primary_key=True
    )
    template_config_name: str
    config_meta: dict[str, typing.Any] = sqlmodel.Field(  # type: ignore
        default={}, sa_column=sqlmodel.Column(sqlmodel.JSON)
    )

    font_id: pydantic.UUID1 = sqlmodel.Field(  # type: ignore
        default=None, foreign_key="fonts.font_id"
    )
    template_id: pydantic.UUID1 = sqlmodel.Field(  # type: ignore
        default=None, foreign_key="ecert_templates.template_id"
    )

    class Config(sqlmodel.SQLModel.Config):
        arbitrary_types_allowed = True

    @classmethod
    @orm.declared_attr
    def __tablename__(cls):
        return "template_configurations"
