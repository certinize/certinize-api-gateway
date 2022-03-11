from starlite import Starlite

from app.api.api_v1 import user_router
from app.core.config import settings
from app.core.events import get_start_app_handler, get_stop_app_handler


def get_application() -> Starlite:
    app = Starlite(
        route_handlers=[user_router],
        debug=settings.debug,
        on_shutdown=[get_stop_app_handler],
        on_startup=[
            settings.logging_config.configure,
            get_start_app_handler,
        ],
        openapi_config=settings.openapi_config,
    )

    return app


app = get_application()
