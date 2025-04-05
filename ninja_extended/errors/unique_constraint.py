"""Module error.unique_constraint."""

from decimal import Decimal
from typing import Literal

from ninja_extended.errors.with_fields import WithFieldsError, WithFieldsErrorResponse


class UniqueConstraintErrorResponse(WithFieldsErrorResponse):
    """UniqueConstraint error response class."""

    type: Literal["errors/unique-constraint"]
    status: Literal[422]


class UniqueConstraintError(WithFieldsError):
    """UniqueConstraint error class."""

    status: int = 422
    schema = UniqueConstraintErrorResponse

    def __init__(
        self,
        fields: dict[str, bool | Decimal | float | int | str | None],
    ):
        """Initialize an UniqueConstraintError."""

        super().__init__(type="errors/unique-constraint", fields=fields)


def unique_constraint_error_factory(resource_: str):
    """Get a resource specific UniqueConstraintError class."""

    class Error(UniqueConstraintError):
        resource = resource_

    return Error
