import pydantic
import sqlmodel
from sqlalchemy import orm


class Templates(sqlmodel.SQLModel, table=True):
    template_id: pydantic.UUID1 | None = sqlmodel.Field(  # type: ignore
        default=None, primary_key=True
    )
    api_key: pydantic.UUID5 | None = sqlmodel.Field(default=None)  # type: ignore
    template_url: pydantic.HttpUrl
    template_height: int
    template_width: int
    template_path: str | None
    template_name: str | None
    template_size: pydantic.ByteSize | None
    template_thumbnail_url: pydantic.HttpUrl | None

    @classmethod
    @orm.declared_attr
    def __tablename__(cls):
        return "certificate_templates"
