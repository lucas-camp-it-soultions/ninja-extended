"""Module error.check_constraint."""

from decimal import Decimal
from typing import Literal

from ninja_extended.errors.base import APIError, APIErrorResponse


class CheckConstraintErrorResponse(APIErrorResponse):
    """CheckConstraint error response class."""

    type: Literal["errors/check-constraint"]
    status: Literal[422]
    resource: str


class CheckConstraintError(APIError):
    """CheckConstraint error class."""

    resource: str
    status: int = 422
    schema = CheckConstraintErrorResponse

    def __init__(
        self,
    ):
        """Initialize an CheckConstraintError."""

        super().__init__(type="errors/check-constraint")

    def to_dict(self):
        """Serialize the CheckConstraintError."""

        base_dict = super().to_dict()
        base_dict.update(
            {
                "resource": self.resource,
            }
        )

        return base_dict
