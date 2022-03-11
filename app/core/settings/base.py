# type: ignore
from enum import Enum

from pydantic import BaseSettings


class AppEnv(Enum):
    prod: str = "prod"
    dev: str = "dev"


class BaseAppSettings(BaseSettings):
    app_env: AppEnv = AppEnv.prod

    class Config:
        env_file = ".env"
