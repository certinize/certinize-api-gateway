import asyncio
import typing
import uuid

from sqlalchemy import exc
from sqlalchemy.ext import asyncio as sqlalchemy_asyncio

from app.api.api_v1.routes.services import configuration
from app.core import abc
from app.db import crud
from app.models.domain import certificate
from app.models.schemas import certificates
from app.services import object_processor


class CertificateService:  # pylint: disable=R0903
    async def _generate_certificate(  # pylint: disable=R0913
        self,
        data: certificate.CertificateTemplateMeta,
        database: crud.DatabaseImpl,
        object_processor_: object_processor.ObjectProcessor,
        template_config: dict[str, typing.Any],
        request_id: uuid.UUID,
        /,
    ):
        conf_ = template_config["template_config"]["config_meta"]
        certificate_meta = certificate_meta = {
            "recipient_name_meta": conf_["recipient_name_meta"],
            "template_url": template_config["template"]["template_url"],
            "issuance_date": data.issuance_date,
            "recipients": data.recipients,
        }
        result = await object_processor_.generate_certificate(certificate_meta)
        print(result)
        content = result[0]

        await database.add(
            certificates.Certificates(
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
        config_service: configuration.ConfigurationService,
        data: certificate.CertificateTemplateMeta,
        database: crud.DatabaseImpl,
        configuration_repo: abc.Database,
        engine: sqlalchemy_asyncio.AsyncEngine,
        object_processor_: object_processor.ObjectProcessor,
        request_id: uuid.UUID,
        token: str,
        /,
    ) -> None:
        template_config = await config_service.get_template_config(
            configuration_repo, engine, data.template_config_id, token
        )

        # Spawning a task here rather than in the controller allows us to raise a 404
        # when no template config is found.
        asyncio.create_task(
            self._generate_certificate(
                data,
                database,
                object_processor_,
                template_config,
                request_id,
            )
        )

    async def get_certificate(
        self,
        certificate_id: uuid.UUID,
        collections_schema: type[certificates.Certificates],
        database: crud.DatabaseImpl,
        /,
    ) -> dict[str, typing.Any]:
        result = await database.select(
            collections_schema(certificate_id=certificate_id),
            "certificate_id",
            str(certificate_id),
        )

        try:
            return result.one().dict()
        except exc.NoResultFound as err:
            return {"detail": str(err), "code": 404}
