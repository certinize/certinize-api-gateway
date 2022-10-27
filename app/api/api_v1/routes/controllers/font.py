import typing

import pydantic
import starlite

from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.routes.services import font as service
from app.db import crud
from app.models.schemas import fonts

AllFonts: typing.TypeAlias = dict[str, list[dict[str, str]]]


class FontController(starlite.Controller):
    path = "/fonts"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "database": starlite.Provide(database_deps.get_db_impl),
        "font_schema": starlite.Provide(database_deps.get_fonts_schema),
        "fonts_service": starlite.Provide(service.FontService),
    }

    @starlite.get()
    async def get_all_fonts(
        self,
        database: crud.DatabaseImpl,
        font_schema: type[fonts.Fonts],
        fonts_service: service.FontService,
    ) -> AllFonts:
        return await fonts_service.get_all_fonts(
            database=database, font_schema=font_schema
        )

    @starlite.get(path="/{font_id:uuid}")
    async def get_font(
        self,
        database: crud.DatabaseImpl,
        font_id: pydantic.UUID1,
        font_schema: type[fonts.Fonts],
        fonts_service: service.FontService,
    ) -> dict[str, typing.Any]:
        return await fonts_service.get_font(
            database=database, font_id=font_id, font_schema=font_schema
        )
