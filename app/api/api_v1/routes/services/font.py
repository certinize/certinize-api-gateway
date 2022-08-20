import pydantic

from app.db import crud
from app.models.schemas import fonts


class FontService:  # pylint: disable=R0903
    async def get_all_fonts(
        self, database: crud.DatabaseImpl, font_schema: type[fonts.Fonts]
    ) -> dict[str, list[dict[str, str]]]:
        result = await database.select_all_row(
            font_schema(
                font_url=pydantic.HttpUrl(scheme="http", url="http://example.com")
            )
        )
        return {"fonts": result.all()}
