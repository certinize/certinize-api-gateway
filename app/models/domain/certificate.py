import datetime

import pydantic


class CertificateTemplateMeta(pydantic.BaseModel):
    recipient_name_meta: dict[str, int | dict[str, float]]
    issuance_date_meta: dict[str, int | dict[str, float]]
    template_url: pydantic.HttpUrl
    font_url: pydantic.HttpUrl
    issuance_date: datetime.date
    recipients: list[dict[str, str]]
