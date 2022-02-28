"""
NOTE: Returning custom HTTP errors using starlite (1.2.3) is currently difficult.
"""
from app.api.api_v1.errors.exceptions import (
    RequestValidationError as RequestValidationError,
)
from app.api.api_v1.errors.validation_error import (
    http422_error_handler as http422_error_handler,
)
