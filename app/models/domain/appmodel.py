from pydantic import BaseConfig


class AppModel:
    class Config(BaseConfig):
        anystr_strip_whitespace = True
