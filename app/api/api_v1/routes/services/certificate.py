import typing
import uuid

import sortedcontainers

from app.api.api_v1.routes.services import configuration
from app.db import crud
from app.models.domain import certificate
from app.models.schemas import certificates, configurations, fonts, templates
from app.services import image_processor


class CertificateService:  # pylint: disable=R0903
    async def generate_certificate(  # pylint: disable=R0913
        self,
        collections_schema: type[certificates.Certificates],
        config_service: configuration.ConfigurationService,
        configs_schema: type[configurations.Configurations],
        data: certificate.CertificateTemplateMeta,
        database: crud.DatabaseImpl,
        fonts_schema: type[fonts.Fonts],
        image_processor_: image_processor.ImageProcessor,
        templates_schema: type[templates.Templates],
    ) -> dict[str, typing.Any]:
        template_config = await config_service.get_template_config(
            template_config_id=data.template_config_id,
            configs_schema=configs_schema,
            templates_schema=templates_schema,
            fonts_schema=fonts_schema,
            database=database,
        )

        certificate_meta = {
            "recipient_name_meta": {"position": {"x": 522, "y": 420}, "font_size": 64},
            "issuance_date_meta": {"position": {"x": 310, "y": 514}, "font_size": 48},
            "template_url": template_config["template"]["template_url"],
            "font_url": template_config["font"]["font_url"],
            "issuance_date": data.issuance_date,
            "recipients": data.recipients,
        }

        result = await image_processor_.generate_certificate(
            certificate_meta=certificate_meta
        )

        certificate_id = uuid.uuid1()

        await database.add_row(
            collections_schema(
                certificate_id=certificate_id,
                certificate=result,
                template_config_id=data.template_config_id,
            )
        )

        result["certificate_id"] = certificate_id
        result["template_config_id"] = data.template_config_id

        return dict(sortedcontainers.SortedDict(result))
