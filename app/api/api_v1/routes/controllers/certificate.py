import typing
import uuid

import starlite

from app.api.api_v1.dependencies import database
from app.api.api_v1.routes.services import certificate as service
from app.db import crud
from app.models.domain import certificate
from app.models.schemas import certificates


class CertificateController(starlite.Controller):
    path = "/certificates"

    dependencies: typing.Optional[dict[str, "starlite.Provide"]] = {
        "certificate_service": starlite.Provide(service.CertificateService),
        "database": starlite.Provide(database.get_db_impl),
    }

    @starlite.post(
        path="save",
        dependencies={
            "certificate_config_schema": starlite.Provide(
                database.get_certificate_config_schema
            )
        },
    )
    async def save(
        self,
        data: certificate.CertificateConfigSave,
        certificate_service: service.CertificateService,
        certificate_config_schema: type[certificates.CertificateConfiguration],
        database: crud.DatabaseImpl,
    ) -> dict[str, uuid.UUID | typing.Any]:
        certificate_config = await certificate_service.save(
            data, certificate_config_schema, database
        )

        return certificate_config

        # return response.CertificateStorageResponse(
        #     template_config_id=uuid.uuid1(),
        #     template_id=uuid.uuid1(),
        #     recipient_name={},
        #     issuance_date={},
        # )

    # @starlite.get(path="configure")
    # async def configure(self):
    #     ...

    # @starlite.post(path="generate")
    # async def generate(self):
    #     ...

    # @starlite.get(path="transfer")
    # async def transfer(self):
    #     ...

    # @starlite.get(path="verify")
    # async def verify(self, certificate_id: uuid.UUID):
    #     ...
