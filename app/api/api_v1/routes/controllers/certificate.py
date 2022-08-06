import typing

import starlite

from app.api.api_v1.routes.services import certificate as service
from app.models.domain import certificate


class CertificateController(starlite.Controller):
    path = "/certificates"

    dependencies: typing.Optional[dict[str, "starlite.Provide"]] = {
        "certificate_service": starlite.Provide(service.CertificateService)
    }

    @starlite.post(path="save")
    async def save(
        self, data: certificate.CertificateStorage
    ) -> certificate.CertificateStorage:
        return data

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
