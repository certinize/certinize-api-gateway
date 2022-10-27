import uuid

import pydantic

from app.models.domain import app_model


class Position(app_model.AppModel):
    x: int
    y: int


class TextPostionMeta(app_model.AppModel):
    position: Position
    font_size: int
    font_url: pydantic.HttpUrl


class TemplateConfiguration(app_model.AppModel):
    recipient_name_meta: TextPostionMeta
    issuance_date_meta: TextPostionMeta
    template_id: uuid.UUID
    template_config_name: str
