"""Module error.multiple_objects_returned."""

from decimal import Decimal
from typing import Literal

from ninja_extended.errors.with_fields import WithFieldsError, WithFieldsErrorResponse


class MultipleObjectsReturnedErrorResponse(WithFieldsErrorResponse):
    """MultipleObjectsReturned error response class."""

    type: Literal["errors/multiple-objects-returned"]
    status: Literal[422]


class MultipleObjectsReturnedError(WithFieldsError):
    """MultipleObjectsReturned error class."""

    status: int = 422
    schema = MultipleObjectsReturnedErrorResponse

    def __init__(
        self,
        fields: dict[str, bool | Decimal | float | int | str | None],
    ):
        """Initialize a MultipleObjectsReturnedError."""

        super().__init__(type="errors/multiple-objects-returned", fields=fields)
