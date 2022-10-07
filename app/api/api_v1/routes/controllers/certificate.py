import asyncio
import uuid

import pydantic
import starlite
from sqlalchemy.ext import asyncio as sqlalchemy_asyncio

from app.api.api_v1.dependencies import associated_services
from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.routes.services import certificate as cert_service
from app.api.api_v1.routes.services import configuration as config_service
from app.db import crud
from app.db.repositories import configurations as config_repo_
from app.models.domain import certificate
from app.models.schemas import certificates, configurations, fonts, templates
from app.services import object_processor


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
        "object_processor_": starlite.Provide(
            associated_services.get_object_processor_client
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
        object_processor_: object_processor.ObjectProcessor,
        templates_schema: type[templates.Templates],
    ) -> starlite.Response[dict[str, pydantic.UUID1]]:
        request_id = uuid.uuid1()

        asyncio.create_task(
            certificate_service.generate_certificate(
                collections_schema=certificate_collections_schema,
                config_repo=config_repo,
                config_service=config_service_,
                configs_schema=configs_schema,
                data=data,
                database=database,
                engine=engine,
                fonts_schema=fonts_schema,
                object_processor_=object_processor_,
                templates_schema=templates_schema,
                request_id=request_id,
            )
        )

        return starlite.Response(
            status_code=202,
            content={"request_id": request_id},
            media_type="application/json",
        )

    @starlite.get("/{request_id:uuid}")
    async def get_certificate(
        self,
        request_id: uuid.UUID,
        database: crud.DatabaseImpl,
        certificate_service: cert_service.CertificateService,
        certificate_collections_schema: type[certificates.Certificates],
    ) -> starlite.Response[dict[str, str]]:
        result = await certificate_service.get_certificate(
            request_id, certificate_collections_schema, database
        )

        return starlite.Response(
            status_code=result.get("code") or 200,
            content=result,
            media_type="application/json",
        )
