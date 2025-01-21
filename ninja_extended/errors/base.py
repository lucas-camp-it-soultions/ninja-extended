"""Module errors.base."""

from django.http import HttpRequest
from pydantic import BaseModel

from ninja_extended.api import ExtendedNinjaAPI


class APIErrorResponse(BaseModel):
    """Schema for base error class."""

    type: str
    status: int
    path: str
    operation_id: str


class APIError(Exception):
    """Base error class."""

    status: int
    schema: type[APIErrorResponse]

    def __init__(self, type: str):  # noqa: A002
        """Initialize an APIError."""

        super().__init__()

        self.type = type

    def to_dict(self):
        """Serialize the APIError."""

        return {
            "type": self.type,
            "status": self.status,
        }


def register_error_handler(api: ExtendedNinjaAPI, error_type: type[APIError]):
    """Register an APIError.

    Args:
        api (ExtendedNinjaAPI): The API to regsiter the error for.
        error_type (type[APIError]): The error type.
    """

    def _handler(request: HttpRequest, error: APIError):
        return api.create_response(
            request=request,
            data=error.schema(**error.to_dict(), path=request.path, operation_id=request.operation_id),
            status=error.status,
        )

    api.add_exception_handler(exc_class=error_type, handler=_handler)
