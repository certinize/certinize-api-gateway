from pydantic import BaseConfig, BaseModel


class AppModel(BaseModel):
    class Config(BaseConfig):
        anystr_strip_whitespace = True
