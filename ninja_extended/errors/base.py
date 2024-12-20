"""Module errors.base."""

from django.http import HttpRequest
from pydantic import BaseModel

from ninja_extended.api import ExtendedNinjaAPI


class APIError(Exception):
    """Base error class."""

    status: int

    def __init__(self, type: str, title: str, detail: str | None):  # noqa: A002
        """Initialize an APIError."""

        super().__init__()

        self.type = type
        self.title = title
        self.detail = detail

    def to_dict(self):
        """Serialize the APIError."""

        return {
            "type": self.type,
            "status": self.status,
            "title": self.title,
            "detail": self.detail,
        }

    @classmethod
    def schema(cls) -> type[BaseModel]:
        """Return the schema for the error.

        Returns:
            type[BaseModel]: The schema.
        """

        raise NotImplementedError("The method 'schema' must be implemented.")  # noqa: EM101


class APIErrorResponse(BaseModel):
    """Schema for base error class."""

    type: str
    status: int
    title: str
    detail: str | None = None
    path: str
    opertaion_id: str


def register_exception_handler(api: ExtendedNinjaAPI, error_type: type[APIError]):
    """Register an APIError.

    Args:
        api (ExtendedNinjaAPI): The API to regsiter the error for.
        error_type (type[APIError]): The error type.
    """

    def _handler(request: HttpRequest, error: APIError):
        return api.create_response(
            request=request,
            data=error.schema()(**error.to_dict(), path=request.path, operation_id=request.operation_id),
            status=error.status,
        )

    api.add_exception_handler(exc_class=error_type, handler=_handler)
