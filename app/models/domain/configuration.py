import typing
import uuid

import pydantic

from app.models.domain import app_model


class TemplateConfiguration(app_model.AppModel):
    recipient_name_meta: dict[str, dict[str, int] | int]
    issuance_date_meta: dict[str, dict[str, int] | int]
    template_id: uuid.UUID
    template_config_name: str
    font_id: uuid.UUID

    @pydantic.root_validator(pre=True)
    @classmethod
    def check_recipient_name_has_position(cls, values: dict[str, typing.Any]):
        try:
            _ = values["recipient_name_meta"]["position"]
            _ = values["issuance_date_meta"]["position"]
        except KeyError as key_err:
            raise ValueError(
                "position key(s) is missing from the request body"
            ) from key_err
        return values

    @pydantic.root_validator(pre=True)
    @classmethod
    def check_position_has_axes(cls, values: dict[str, typing.Any]):
        try:
            _ = values["recipient_name_meta"]["position"]["x"]
            _ = values["recipient_name_meta"]["position"]["y"]
            _ = values["issuance_date_meta"]["position"]["x"]
            _ = values["issuance_date_meta"]["position"]["y"]
        except KeyError as key_err:
            raise ValueError("axes/axis is missing from the request body") from key_err
        return values

    @pydantic.root_validator(pre=True)
    @classmethod
    def check_parent_keys_have_font_size(cls, values: dict[str, typing.Any]):
        try:
            _ = values["recipient_name_meta"]["font_size"]
            _ = values["issuance_date_meta"]["font_size"]
        except KeyError as key_err:
            raise ValueError(
                "font size key(s) is missing from the request body"
            ) from key_err
        return values
