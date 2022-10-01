import typing
import uuid

from sqlalchemy.ext import asyncio as sqlalchemy_asyncio

from app.api.api_v1.routes.services import configuration
from app.db import crud
from app.db.repositories import configurations as config_repo_
from app.models.domain import certificate
from app.models.schemas import certificates, configurations, fonts, templates
from app.services import object_processor


class CertificateService:  # pylint: disable=R0903
    async def _generate_certificate(  # pylint: disable=R0913
        self,
        collections_schema: type[certificates.Certificates],
        data: certificate.CertificateTemplateMeta,
        database: crud.DatabaseImpl,
        object_processor_: object_processor.ObjectProcessor,
        template_config: dict[str, typing.Any],
        request_id: uuid.UUID,
    ):
        conf_ = template_config["template_config"]["config_meta"]
        result = await object_processor_.generate_certificate(
            certificate_meta={
                "recipient_name_meta": conf_["recipient_name_meta"],
                "issuance_date_meta": conf_["issuance_date_meta"],
                "template_url": template_config["template"]["template_url"],
                "font_url": template_config["font"]["font_url"],
                "issuance_date": data.issuance_date,
                "recipients": data.recipients,
            }
        )
        content = result[0]

        await database.add_row(
            collections_schema(
                certificate_id=request_id,
                certificate=content,
                template_config_id=data.template_config_id,
            )
        )

        content["certificate_id"] = request_id
        content["template_config_id"] = data.template_config_id

        return content, result[1]

    async def generate_certificate(  # pylint: disable=R0913
        self,
        collections_schema: type[certificates.Certificates],
        config_repo: config_repo_.ConfigurationsRepository,
        config_service: configuration.ConfigurationService,
        configs_schema: type[configurations.Configurations],
        data: certificate.CertificateTemplateMeta,
        database: crud.DatabaseImpl,
        engine: sqlalchemy_asyncio.AsyncEngine,
        fonts_schema: type[fonts.Fonts],
        object_processor_: object_processor.ObjectProcessor,
        templates_schema: type[templates.Templates],
        request_id: uuid.UUID,
    ) -> tuple[dict[str, typing.Any], int]:
        template_config = await config_service.get_template_config(
            template_config_id=data.template_config_id,
            configs_schema=configs_schema,
            templates_schema=templates_schema,
            fonts_schema=fonts_schema,
            database=config_repo,
            engine=engine,
        )

        return await self._generate_certificate(
            collections_schema=collections_schema,
            data=data,
            database=database,
            object_processor_=object_processor_,
            template_config=template_config,
            request_id=request_id,
        )
