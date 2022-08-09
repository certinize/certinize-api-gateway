import pydantic


class AppModel(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        anystr_strip_whitespace = True
