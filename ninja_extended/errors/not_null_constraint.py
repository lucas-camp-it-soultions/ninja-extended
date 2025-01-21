"""Module error.not_null_constraint."""

from decimal import Decimal
from typing import Literal

from ninja_extended.errors.with_fields import WithFieldsError, WithFieldsErrorResponse


class NotNullConstraintErrorResponse(WithFieldsErrorResponse):
    """NotNullConstraint error response class."""

    type: Literal["errors/not-null-constraint"]
    status: Literal[422]


class NotNullConstraintError(WithFieldsError):
    """NotNullConstraint error class."""

    status: int = 422
    schema = NotNullConstraintErrorResponse

    def __init__(
        self,
        fields: dict[str, bool | Decimal | float | int | str | None],
    ):
        """Initialize an NotNullConstraintError."""

        super().__init__(type="errors/not-null-constraint", fields=fields)
