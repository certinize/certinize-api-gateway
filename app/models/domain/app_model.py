import typing

import pydantic


class AppModel(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        anystr_strip_whitespace = True

    @classmethod
    def with_fields(cls, **field_definitions: typing.Any) -> type[pydantic.BaseModel]:
        return pydantic.create_model(
            "ModelWithFields", __base__=cls, **field_definitions
        )
