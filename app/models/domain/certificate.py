import typing
import uuid

import pydantic

from app.models.domain import app_model


class CertificateStorage(app_model.AppModel):
    recipient_name: dict[str, dict[str, int] | int]
    issuance_date: dict[str, dict[str, int] | int]
    template_id: uuid.UUID

    @pydantic.root_validator(pre=True)
    def check_recipient_name_has_position(cls, values: dict[str, typing.Any]):
        try:
            values["recipient_name"]["position"]
            values["issuance_date"]["position"]
        except KeyError as key_err:
            raise ValueError(
                "position key(s) is missing from the request body"
            ) from key_err
        return values

    @pydantic.root_validator(pre=True)
    def check_position_has_axes(cls, values: dict[str, typing.Any]):
        try:
            values["recipient_name"]["position"]["x"]
            values["recipient_name"]["position"]["y"]
            values["issuance_date"]["position"]["x"]
            values["issuance_date"]["position"]["y"]
        except KeyError as key_err:
            raise ValueError("axes/axis is missing from the request body") from key_err
        return values

    @pydantic.root_validator(pre=True)
    def check_parent_keys_have_font_size(cls, values: dict[str, typing.Any]):
        try:
            values["recipient_name"]["font_size"]
            values["issuance_date"]["font_size"]
        except KeyError as key_err:
            raise ValueError(
                "font size key(s) is missing from the request body"
            ) from key_err
        return values


class CertificateConfiguration(app_model.AppModel):
    ...


class CertificateGeneration(app_model.AppModel):
    ...


class CertificateTransfer(app_model.AppModel):
    ...


class CertificateVerification(app_model.AppModel):
    ...
