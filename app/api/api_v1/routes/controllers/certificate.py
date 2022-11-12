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
from app.models.schemas import certificates
from app.services import object_processor


class CertificateController(starlite.Controller):
    path = "/certificates"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "engine": starlite.Provide(database_deps.get_db_engine),
        "certificate_service": starlite.Provide(cert_service.CertificateService),
        "config_repo": starlite.Provide(database_deps.get_configurations_repository),
        "config_service_": starlite.Provide(config_service.ConfigurationService),
        "database": starlite.Provide(database_deps.get_db_impl),
        "object_processor_": starlite.Provide(
            associated_services.get_object_processor_client
        ),
    }

    @starlite.post()
    async def generate_certificate(  # pylint: disable=R0913
        self,
        certificate_service: cert_service.CertificateService,
        config_service_: config_service.ConfigurationService,
        config_repo: config_repo_.ConfigurationsRepository,
        data: certificate.CertificateTemplateMeta,
        database: crud.DatabaseImpl,
        engine: sqlalchemy_asyncio.AsyncEngine,
        object_processor_: object_processor.ObjectProcessor,
        token: str = starlite.Parameter(header="X-API-KEY", min_length=36),
    ) -> starlite.Response[dict[str, pydantic.UUID1]]:
        request_id = uuid.uuid1()

        await certificate_service.generate_certificate(
            config_service_,
            data,
            database,
            config_repo,
            engine,
            object_processor_,
            request_id,
            token,
        )

        return starlite.Response(
            status_code=202,
            content={"request_id": request_id},
            media_type="application/json",
        )

    @starlite.get("/{request_id:uuid}")
    async def get_certificate(  # pylint: disable=R0913
        self,
        request_id: uuid.UUID,
        database: crud.DatabaseImpl,
        certificate_service: cert_service.CertificateService,
        token: str = starlite.Parameter(header="X-API-KEY", min_length=36),
    ) -> starlite.Response[dict[str, str]]:
        # Temporarily ignore the token until we implement a repository for certificates
        _ = token

        result = await certificate_service.get_certificate(
            request_id, certificates.Certificates, database
        )

        return starlite.Response(
            status_code=result.get("code") or 200,
            content=result,
            media_type="application/json",
        )
