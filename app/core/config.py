from functools import lru_cache
from typing import Type

from app.core.settings.app import AppSettings
from app.core.settings.base import AppEnv, BaseAppSettings
from app.core.settings.dev import DevAppSettings
from app.core.settings.prod import ProdAppSettings

environments: dict[AppEnv, Type[AppSettings]] = {
    AppEnv.DEV: DevAppSettings,
    AppEnv.PROD: ProdAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()


settings = get_app_settings()
