import typing

import starlite

from app.api.api_v1.dependencies import database
from app.api.api_v1.dependencies import image_processor as image_processor_deps
from app.api.api_v1.routes.services import certificate as cert_service
from app.db import crud
from app.models.domain import certificate
from app.models.schemas import certificates
from app.services import image_processor


class CertificateController(starlite.Controller):
    path = "/certificates"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "database_": starlite.Provide(database.get_db_impl),
        "certificate_service": starlite.Provide(cert_service.CertificateService),
        "image_processor_": starlite.Provide(
            image_processor_deps.get_image_processor_client
        ),
        "certificate_collections_schema": starlite.Provide(
            database.get_certificate_collections_schema
        ),
    }

    @starlite.post()
    async def generate_certificate(  # pylint: disable=R0913
        self,
        data: certificate.CertificateTemplateMeta,
        database_: crud.DatabaseImpl,
        certificate_service: cert_service.CertificateService,
        image_processor_: image_processor.ImageProcessor,
        certificate_collections_schema: type[certificates.CertificateCollections],
    ) -> typing.Any:
        return await certificate_service.generate_certificate(
            certificate_collections_schema=certificate_collections_schema,
            data=data,
            database=database_,
            image_processor_=image_processor_,
        )
