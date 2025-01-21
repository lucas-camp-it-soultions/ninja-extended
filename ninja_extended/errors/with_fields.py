"""Module error.with_fields."""

from decimal import Decimal

from ninja_extended.errors.base import APIError, APIErrorResponse


class WithFieldsErrorResponse(APIErrorResponse):
    """WithFields error response class."""

    resource: str
    fields: dict[str, bool | Decimal | float | int | str | None]


class WithFieldsError(APIError):
    """Base error class that has fields argument."""

    resource: str
    status: int

    def __init__(
        self,
        type: str,  # noqa: A002
        fields: dict[str, bool | Decimal | float | int | str | None],
    ):
        """Initialize a WithFieldsError."""

        super().__init__(type=type)

        self.fields = fields

    def to_dict(self):
        """Serialize the WithFieldsError."""

        base_dict = super().to_dict()
        base_dict.update(
            {
                "fields": self.fields,
                "resource": self.resource,
            }
        )

        return base_dict
