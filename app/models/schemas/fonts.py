import pydantic
import sqlmodel


class Fonts(sqlmodel.SQLModel, table=True):
    font_id: pydantic.UUID1 | None = sqlmodel.Field(  # type: ignore
        default=None, primary_key=True
    )
    font_url: pydantic.HttpUrl
    font_name: str
