from starlite import Router

from app.api.api_v1.routes.controllers import user

user_router = Router(path="/", route_handlers=[user.UserController])
