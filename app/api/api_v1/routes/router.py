from starlite import Router

from app.api.api_v1.routes.user import UserController

user_router = Router(path="/", route_handlers=[UserController])
