"""Module error.not_found."""

from typing import Any, Literal

from django.http import HttpRequest
from ninja.errors import ValidationError as NinjaValidationError
from pydantic import BaseModel, Field

from ninja_extended.api.api import ExtendedNinjaAPI
from ninja_extended.errors.base import APIError, APIErrorResponse


class ValidationErrorDetailResponse(BaseModel):
    """Schema for Ninja ValidationError."""

    type: str
    loc: tuple[str | int, ...]
    msg: str
    ctx: dict[str, Any] | None = Field(default=None)


class ValidationErrorResponse(APIErrorResponse):
    """Validation error response class."""

    type: Literal["errors/validation"]
    status: Literal[422]
    errors: list[ValidationErrorDetailResponse]


class ValidationError(APIError):
    """ValidationError error class."""

    status: int = 422
    schema = ValidationErrorResponse

    def __init__(self, errors: list[ValidationErrorDetailResponse]):
        """Initialize a ValidationError."""

        super().__init__(type="errors/validation")

        self.errors = errors

    def to_dict(self):
        """Serialize the NotFoundError."""

        base_dict = super().to_dict()
        base_dict.update({"errors": self.errors})

        return base_dict


def register_validation_error_handler(api: ExtendedNinjaAPI):
    """Register the validation error handler.

    Args:
        api (ExtendedNinjaAPI): The API to regsiter the error for.
    """

    def _handler(request: HttpRequest, error: NinjaValidationError):
        return api.create_response(
            request=request,
            data=ValidationError.schema(
                **ValidationError(errors=error.errors).to_dict(), path=request.path, operation_id=request.operation_id
            ),
            status=422,
        )

    api.add_exception_handler(exc_class=NinjaValidationError, handler=_handler)
