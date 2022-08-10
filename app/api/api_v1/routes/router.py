from starlite import Router

from app.api.api_v1.routes.controllers import (
    certificate,
    configuration,
    issuance,
    template,
    user,
)

api_v1_router = Router(
    path="/api/v1",
    route_handlers=[
        certificate.CertificateController,
        configuration.ConfigurationController,
        issuance.IssuanceController,
        template.TemplateController,
        user.UserController,
    ],
)
