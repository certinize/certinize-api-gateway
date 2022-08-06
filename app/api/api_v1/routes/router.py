from starlite import Router

from app.api.api_v1.routes.controllers import certificate, user

user_router = Router(path="/", route_handlers=[user.UserController])
certificate_router = Router(
    path="/", route_handlers=[certificate.CertificateController]
)
