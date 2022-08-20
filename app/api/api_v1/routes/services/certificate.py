from app.db import crud
from app.models.domain import certificate
from app.models.schemas import certificates
from app.services import image_processor


class CertificateService:
    async def generate_certificate(
        self,
        certificate_collections_schema: type[certificates.CertificateCollections],
        data: certificate.CertificateTemplateMeta,
        database: crud.DatabaseImpl,
        image_processor_: image_processor.ImageProcessor,
    ):
        return await image_processor_.generate_certificate(
            certificate_template_meta=data
        )
