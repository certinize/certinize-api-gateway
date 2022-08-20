import pydantic
import sqlmodel
from sqlalchemy import orm


class CertificateCollections(sqlmodel.SQLModel, table=True):  # pylint: disable=R0913
    collection_id: pydantic.UUID1 | None = sqlmodel.Field(  # type: ignore
        default=None, primary_key=True
    )
    collection: dict[str, list[dict[str, str]]] = sqlmodel.Field(  # type: ignore
        default={}, sa_column=sqlmodel.Column(sqlmodel.JSON)
    )

    class Config(sqlmodel.SQLModel.Config):  # pylint: disable=R0903
        arbitrary_types_allowed = True

    @classmethod
    @orm.declared_attr
    def __tablename__(cls):
        return "certificate_collections"
