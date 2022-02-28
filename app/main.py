from starlite import LoggingConfig, Starlite

from app.api.api_v1 import user_router

logging_config = LoggingConfig(
    loggers={
        "app": {
            "level": "INFO",
            "handlers": ["console"],
        }
    }
)

app = Starlite(
    route_handlers=[user_router],
    on_startup=[logging_config.configure],
)
