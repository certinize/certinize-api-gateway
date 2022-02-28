from typing import Any, Mapping

from starlette.status import HTTP_400_BAD_REQUEST
from starlite import HTTPException, MediaType, Request, Response


def http422_error_handler(
    _: Request[Mapping[Any, Any], Any], exc: Exception | HTTPException
) -> Response:
    status_code = HTTP_400_BAD_REQUEST
    detail = ""
    extra = None
    if hasattr(exc, "detail"):
        detail = exc.detail  # type: ignore
    if hasattr(exc, "status_code"):
        status_code = exc.status_code  # type: ignore
    if hasattr(exc, "status_code"):
        extra = exc.extra  # type: ignore

    return Response(
        media_type=MediaType.JSON,
        content={"detail": detail, "extra": extra},
        status_code=status_code,  # type: ignore
    )
