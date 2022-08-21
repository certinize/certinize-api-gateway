import pydantic
import sqlmodel


class Certificates(sqlmodel.SQLModel, table=True):  # pylint: disable=R0913
    certificate_id: pydantic.UUID1 | None = sqlmodel.Field(  # type: ignore
        default=None, primary_key=True
    )
    certificate: dict[str, list[dict[str, str]]] = sqlmodel.Field(  # type: ignore
        default={}, sa_column=sqlmodel.Column(sqlmodel.JSON)
    )
    template_config_id: pydantic.UUID1 = sqlmodel.Field(  # type: ignore
        default=None, foreign_key="template_configurations.template_config_id"
    )

    class Config(sqlmodel.SQLModel.Config):  # pylint: disable=R0903
        arbitrary_types_allowed = True
