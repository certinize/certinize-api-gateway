from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from starlite import HTTPException


class RequestError(Exception):
    ...


class RequestValidationError(HTTPException, RequestError):
    status_code = HTTP_422_UNPROCESSABLE_ENTITY
