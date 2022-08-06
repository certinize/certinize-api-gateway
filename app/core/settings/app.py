from pydantic import PostgresDsn
from starlite import LoggingConfig, OpenAPIConfig

from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    debug: bool = False
    title: str = "Certinize client back-end"
    version: str = "0.1.0"
    openapi_config = OpenAPIConfig(title=title, version=version)

    database_url: PostgresDsn
    max_connection_count: int = 10
    min_connection_count: int = 10

    logging_level = "INFO"

    class Config:  # type: ignore
        validate_assignment = True

    @property
    def logging_config(self) -> LoggingConfig:
        return LoggingConfig(
            loggers={
                "app": {
                    "level": self.logging_level,
                    "handlers": ["console"],
                }
            }
        )

    @property
    def sqlalchemy_kwargs(self) -> dict[str, bool | int]:
        return {
            "echo": self.debug,
            "future": True,
            "pool_size": self.min_connection_count,
            "max_overflow": self.max_connection_count,
            "echo_pool": self.debug,
        }
