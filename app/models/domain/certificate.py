import datetime
import uuid

import pydantic


class CertificateTemplateMeta(pydantic.BaseModel):
    template_config_id: uuid.UUID
    issuance_date: datetime.date
    recipients: list[dict[str, str]]
