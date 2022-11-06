import uuid

import pydantic

from app.db import crud
from app.models.schemas import fonts


class FontService:  # pylint: disable=R0903
    async def get_all_fonts(
        self, database: crud.DatabaseImpl, font_schema: type[fonts.Fonts]
    ) -> dict[str, list[dict[str, str]]]:
        result = await database.select_all(
            font_schema(
                font_url=pydantic.HttpUrl(scheme="http", url="http://example.com"),
                font_name="",
            )
        )
        return {"fonts": result.all()}

    async def get_font(
        self,
        database: crud.DatabaseImpl,
        font_schema: type[fonts.Fonts],
        font_id: uuid.UUID,
    ) -> dict[str, dict[str, str]]:
        result = await database.select(
            font_schema(
                font_id=font_id,
                font_url=pydantic.HttpUrl(scheme="http", url="http://example.com"),
                font_name="",
            ),
            "font_id",
            str(font_id),
        )

        return {"font": result.one()}
