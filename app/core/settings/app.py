import typing

import pydantic
import starlite

from app.core.settings import base


class AppSettings(base.BaseAppSettings):
    debug = False
    title = "Certinize client back-end"
    version = "0.1.0"
    openapi_config = starlite.OpenAPIConfig(title=title, version=version)

    database_url: typing.Optional[pydantic.PostgresDsn] = None
    max_connection_count = 10
    min_connection_count = 10

    s3_api_endpoint_url: pydantic.AnyHttpUrl = pydantic.AnyHttpUrl(
        url="https://", scheme="https"
    )
    s3_secret_access_key = ""
    s3_access_key_id = ""

    imagekit_endpoint_url: pydantic.AnyHttpUrl = pydantic.AnyHttpUrl(
        url="https://", scheme="https"
    )
    imagekit_public_key = ""
    imagekit_private_key = ""

    logging_level = "INFO"

    class Config(base.BaseAppSettings.Config):
        validate_assignment = True

    @property
    def logging_config(self) -> starlite.LoggingConfig:
        return starlite.LoggingConfig(
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
