import uuid

import pydantic


class CertificateTemplateMeta(pydantic.BaseModel):
    template_config_id: uuid.UUID
    recipients: list[dict[str, str]]
