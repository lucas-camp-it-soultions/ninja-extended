"""Module error.check_constraint."""

from typing import Literal

from django.db.models import ProtectedError as DjangoProtectedError

from ninja_extended.errors.base import APIError, APIErrorResponse


class ProtectedErrorResponse(APIErrorResponse):
    """Protected error response class."""

    type: Literal["errors/protection"]
    status: Literal[422]
    resource: str
    foreign_items: dict[str, list[int]]


class ProtectedError(APIError):
    """Protected error class."""

    resource: str
    status: int = 422
    schema = ProtectedErrorResponse

    def __init__(
        self,
        foreign_items: dict[str, list[int]],
    ):
        """Initialize an ProtectedError."""

        super().__init__(type="errors/protection")
        self.foreign_items = foreign_items

    def to_dict(self):
        """Serialize the ProtectedError."""

        base_dict = super().to_dict()
        base_dict.update(
            {
                "resource": self.resource,
                "foreign_items": self.foreign_items,
            }
        )

        return base_dict


def handle_protected_error(
    error: DjangoProtectedError,
    protected_error_type: type[ProtectedError],
):
    """Handle ProtectedError.

    Args:
        error (IntegrityError): The error.
        protected_error_type (type[ProtectedError]): The protected error type.

    Raises:
        protected_error_type: If a protected error have been parsed.
    """

    foreign_items = {}

    for instance in error.protected_objects:
        model_name = type(instance).__name__

        if model_name not in foreign_items:
            foreign_items[model_name] = []

        foreign_items[model_name].append(instance.id)

    for model_name in foreign_items:
        foreign_items[model_name] = sorted(foreign_items[model_name])

    raise protected_error_type(foreign_items=foreign_items)


def protected_error_factory(resource_: str):
    """Get a resource specific ProtectedError class."""

    class Error(ProtectedError):
        resource = resource_

    return Error
