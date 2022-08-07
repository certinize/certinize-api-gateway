import uuid

from app.db import crud
from app.models.domain import certificate
from app.models.schemas import certificates


class CertificateService:
    async def save(
        self,
        data: certificate.CertificateStorage,
        certificate_config_schema: type[certificates.CertificateConfiguration],
        database: crud.DatabaseImpl,
    ):
        await database.add_row(
            certificate_config_schema(
                template_config_id=uuid.uuid1(),
                config_meta=data.__dict__,
            )
        )

    async def configure(self):
        ...

    async def generate(self):
        ...

    async def transfer(self):
        ...

    async def verify(self):
        ...
