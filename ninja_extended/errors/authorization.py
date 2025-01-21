"""Module error.authorization."""

from typing import Literal

from ninja_extended.errors.base import APIError, APIErrorResponse


class AuthorizationErrorResponse(APIErrorResponse):
    """Authorization error response class."""

    type: Literal["errors/authorization"]
    status: Literal[403]
    permissions: list[str]


class AuthorizationError(APIError):
    """Authorization error class."""

    status: int = 403
    schema = AuthorizationErrorResponse

    def __init__(
        self,
        permissions: list[str],
    ):
        """Initialize a AuthorizationError."""

        super().__init__(type="errors/authorization")

        self.permissions = permissions

    def to_dict(self):
        """Serialize the AuthorizationError."""

        base_dict = super().to_dict()
        base_dict.update({"permissions": self.permissions})

        return base_dict
