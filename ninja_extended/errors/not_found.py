"""Module error.not_found."""

from decimal import Decimal
from typing import Literal

from ninja_extended.errors.with_fields import WithFieldsError, WithFieldsErrorResponse


class NotFoundErrorResponse(WithFieldsErrorResponse):
    """NotFound error response class."""

    type: Literal["errors/not-found"]
    status: Literal[404]


class NotFoundError(WithFieldsError):
    """NotFound error class."""

    status: int = 404
    schema = NotFoundErrorResponse

    def __init__(
        self,
        fields: dict[str, bool | Decimal | float | int | str | None],
    ):
        """Initialize a NotFoundError."""

        super().__init__(type="errors/not-found", fields=fields)
