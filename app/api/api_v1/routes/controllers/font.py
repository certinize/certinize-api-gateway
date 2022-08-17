import starlite

from app.api.api_v1.dependencies import database
from app.api.api_v1.routes.services import font as service
from app.db import crud
from app.models.schemas import fonts


class FontController(starlite.Controller):
    path = "/fonts"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "database": starlite.Provide(database.get_db_impl),
        "font_schema": starlite.Provide(database.get_font_schema),
        "fonts_service": starlite.Provide(service.FontService),
    }

    @starlite.get()
    async def get_all_fonts(
        self,
        database: crud.DatabaseImpl,
        font_schema: type[fonts.Fonts],
        fonts_service: service.FontService,
    ) -> dict[str, list[dict[str, str]]]:
        return await fonts_service.get_all_fonts(
            database=database, font_schema=font_schema
        )
