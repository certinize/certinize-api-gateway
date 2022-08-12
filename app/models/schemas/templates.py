import pydantic
import sqlmodel
from sqlalchemy import orm


class Templates(sqlmodel.SQLModel, table=True):
    template_id: pydantic.UUID1 | None = sqlmodel.Field(  # type: ignore
        default=None, primary_key=True
    )
    template_url: pydantic.AnyHttpUrl
    template_height: int
    template_width: int
    template_path: str | None
    template_name: str | None
    template_size: pydantic.ByteSize | None
    template_thumbnail_url: pydantic.AnyHttpUrl | None

    @orm.declared_attr
    @classmethod
    def __tablename__(cls):
        return "ecert_templates"
