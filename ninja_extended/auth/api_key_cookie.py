"""Module auth.api_key_cookie."""

from abc import ABC

from django.http import HttpRequest
from ninja.security.apikey import APIKeyBase
from ninja.utils import check_csrf

from ninja_extended.errors import CSRFError


class APIKeyCookie(APIKeyBase, ABC):
    """APIKeyCookie auth class."""

    openapi_in: str = "cookie"

    def __init__(self, csrf: bool = True) -> None:  # noqa: FBT001, FBT002
        """Initialize an APIKeyCookie."""

        self.csrf = csrf
        super().__init__()

    def _get_key(self, request: HttpRequest) -> str | None:
        if self.csrf:
            error_response = check_csrf(request)
            if error_response:
                raise CSRFError
        return request.COOKIES.get(self.param_name)
