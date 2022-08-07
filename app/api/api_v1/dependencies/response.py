"""
app.api.api_v1.dependencies.schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains a collection of response schemas and samples for api_v1.
"""
import uuid

import pydantic


class AuthResponse(pydantic.BaseModel):
    api_key: uuid.UUID
    user_id: uuid.UUID
    wallet_address: str


class CertificateStorageResponse(pydantic.BaseModel):
    template_config_id: uuid.UUID
    template_id: uuid.UUID
    recipient_name: dict[str, int | dict[str, int]]
    issuance_date: dict[str, int | dict[str, int]]
