import enum

import pydantic


class AppEnv(enum.Enum):
    PROD = "prod"
    DEV = "dev"


class BaseAppSettings(pydantic.BaseSettings):
    app_env: AppEnv = AppEnv.PROD

    class Config(pydantic.BaseSettings.Config):
        env_file = ".env"
