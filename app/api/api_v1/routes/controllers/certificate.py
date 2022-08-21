import typing

import starlite
from sqlalchemy.ext import asyncio as sqlalchemy_asyncio

from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.dependencies import image_processor as image_processor_deps
from app.api.api_v1.routes.services import certificate as cert_service
from app.api.api_v1.routes.services import configuration as config_service
from app.db import crud
from app.db.repositories import configurations as config_repo_
from app.models.domain import certificate
from app.models.schemas import certificates, configurations, fonts, templates
from app.services import image_processor


class CertificateController(starlite.Controller):
    path = "/certificates"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "certificate_collections_schema": starlite.Provide(
            database_deps.get_certificate_collections_schema
        ),
        "engine": starlite.Provide(database_deps.get_db_engine),
        "certificate_service": starlite.Provide(cert_service.CertificateService),
        "config_repo": starlite.Provide(database_deps.get_configurations_repository),
        "config_service_": starlite.Provide(config_service.ConfigurationService),
        "configs_schema": starlite.Provide(
            database_deps.get_certificate_configs_schema
        ),
        "database": starlite.Provide(database_deps.get_db_impl),
        "fonts_schema": starlite.Provide(database_deps.get_fonts_schema),
        "image_processor_": starlite.Provide(
            image_processor_deps.get_image_processor_client
        ),
        "templates_schema": starlite.Provide(database_deps.get_templates_schema),
    }

    @starlite.post()
    async def generate_certificate(  # pylint: disable=R0913
        self,
        certificate_collections_schema: type[certificates.Certificates],
        certificate_service: cert_service.CertificateService,
        config_repo: config_repo_.ConfigurationsRepository,
        config_service_: config_service.ConfigurationService,
        configs_schema: type[configurations.Configurations],
        data: certificate.CertificateTemplateMeta,
        database: crud.DatabaseImpl,
        engine: sqlalchemy_asyncio.AsyncEngine,
        fonts_schema: type[fonts.Fonts],
        image_processor_: image_processor.ImageProcessor,
        templates_schema: type[templates.Templates],
    ) -> typing.Any:
        return await certificate_service.generate_certificate(
            collections_schema=certificate_collections_schema,
            config_repo=config_repo,
            config_service=config_service_,
            configs_schema=configs_schema,
            data=data,
            database=database,
            engine=engine,
            fonts_schema=fonts_schema,
            image_processor_=image_processor_,
            templates_schema=templates_schema,
        )
