import starlite

from app.api.api_v1.routes import router
from app.core import events
from app.core.config import settings


def get_application() -> starlite.Starlite:
    start_app = events.get_start_app_handler()
    stop_app = events.get_stop_app_handler()
    cors_config = starlite.CORSConfig(allow_origins=settings.allow_origins)

    return starlite.Starlite(
        cors_config=cors_config,
        route_handlers=[router.api_v1_router],
        debug=settings.debug,
        on_shutdown=[stop_app],
        on_startup=[
            settings.logging_config.configure,
            start_app,
        ],
        openapi_config=settings.openapi_config,
    )


app = get_application()
