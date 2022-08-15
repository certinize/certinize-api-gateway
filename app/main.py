import starlite

from app.api.api_v1.routes.router import api_v1_router
from app.core.config import settings
from app.core.events import get_start_app_handler, get_stop_app_handler


def get_application() -> starlite.Starlite:
    start_app = get_start_app_handler()
    stop_app = get_stop_app_handler()
    cors_config = starlite.CORSConfig(allow_origins=settings.allow_origins)

    return starlite.Starlite(
        cors_config=cors_config,
        route_handlers=[api_v1_router],
        debug=settings.debug,
        on_shutdown=[stop_app],
        on_startup=[
            settings.logging_config.configure,
            start_app,
        ],
        openapi_config=settings.openapi_config,
    )


app = get_application()
