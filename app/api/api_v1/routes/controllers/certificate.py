import typing

import starlite

from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.dependencies import image_processor as image_processor_deps
from app.api.api_v1.routes.services import certificate as cert_service
from app.api.api_v1.routes.services import configuration as config_service
from app.db import crud
from app.models.domain import certificate
from app.models.schemas import certificates, configurations, fonts, templates
from app.services import image_processor


class CertificateController(starlite.Controller):
    path = "/certificates"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "database": starlite.Provide(database_deps.get_db_impl),
        "certificate_service": starlite.Provide(cert_service.CertificateService),
        "config_service_": starlite.Provide(config_service.ConfigurationService),
        "image_processor_": starlite.Provide(
            image_processor_deps.get_image_processor_client
        ),
        "certificate_collections_schema": starlite.Provide(
            database_deps.get_certificate_collections_schema
        ),
        "configs_schema": starlite.Provide(
            database_deps.get_certificate_configs_schema
        ),
        "fonts_schema": starlite.Provide(database_deps.get_fonts_schema),
        "templates_schema": starlite.Provide(database_deps.get_templates_schema),
    }

    @starlite.post()
    async def generate_certificate(  # pylint: disable=R0913
        self,
        data: certificate.CertificateTemplateMeta,
        database: crud.DatabaseImpl,
        certificate_service: cert_service.CertificateService,
        config_service_: config_service.ConfigurationService,
        image_processor_: image_processor.ImageProcessor,
        certificate_collections_schema: type[certificates.Certificates],
        configs_schema: type[configurations.Configurations],
        fonts_schema: type[fonts.Fonts],
        templates_schema: type[templates.Templates],
    ) -> typing.Any:
        return await certificate_service.generate_certificate(
            collections_schema=certificate_collections_schema,
            configs_schema=configs_schema,
            templates_schema=templates_schema,
            fonts_schema=fonts_schema,
            config_service=config_service_,
            database=database,
            image_processor_=image_processor_,
            data=data,
        )
