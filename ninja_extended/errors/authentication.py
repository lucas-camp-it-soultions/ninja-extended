"""Module error.authentication."""

from typing import Literal

from ninja_extended.errors.base import APIError, APIErrorResponse


class AuthenticationErrorResponse(APIErrorResponse):
    """Authentication error response class."""

    type: Literal["errors/authentication"]
    status: Literal[401]


class AuthenticationError(APIError):
    """Authentication error class."""

    status: int = 401
    schema = AuthenticationErrorResponse

    def __init__(
        self,
    ):
        """Initialize a AuthenticationError."""

        super().__init__(type="errors/authentication")
