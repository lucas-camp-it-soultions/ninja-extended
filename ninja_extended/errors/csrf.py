"""Module error.authentication."""

from typing import Literal

from ninja_extended.errors.base import APIError, APIErrorResponse


class CSRFErrorResponse(APIErrorResponse):
    """CSRF error response class."""

    type: Literal["errors/csrf"]
    status: Literal[403]


class CSRFError(APIError):
    """CSRF error class."""

    status: int = 403
    schema = CSRFErrorResponse

    def __init__(
        self,
    ):
        """Initialize a CSRFError."""

        super().__init__(type="errors/csrf")
