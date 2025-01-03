"""Module auth.session."""

from typing import Any

from django.conf import settings
from django.http import HttpRequest

from ninja_extended.auth.api_key_cookie import APIKeyCookie
from ninja_extended.errors import AuthenticationError, AuthorizationError


class SessionAuth(APIKeyCookie):
    """SessionAuth auth class."""

    param_name: str = settings.SESSION_COOKIE_NAME

    def __init__(self, csrf=True, permissions: list[str] | None = None):  # noqa: FBT002
        """Initialize a SessionAuth."""

        super().__init__(csrf)
        self.permissions = permissions

    def authenticate(self, request: HttpRequest, key: str | None) -> Any | None:  # noqa: ARG002
        """Authenticate a user and check permissions."""

        if request.user.is_authenticated:
            if self.permissions is None:
                return request.user

            if request.user.has_perms(self.permissions):
                return request.user

            return AuthorizationError(permissions=self.permissions)

        return AuthenticationError


def session_auth(permissions: list[str] | None = None):
    """Instantiate auth class with given permissions.

    Args:
        permissions (list[str] | None, optional): The permissions. Defaults to None.

    Returns:
        _type_: The auth class.
    """

    return SessionAuth(permissions=permissions)
