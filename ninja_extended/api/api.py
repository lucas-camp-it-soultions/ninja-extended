"""Module api.api."""

# ruff: noqa: ARG002

import warnings
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any, TypeVar

from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.constants import NOT_SET, NOT_SET_TYPE
from ninja.openapi.docs import DocsBase, Swagger
from ninja.parser import Parser
from ninja.renderers import BaseRenderer, JSONRenderer
from ninja.throttling import BaseThrottle
from ninja.types import DictStrAny, TCallable

from ninja_extended.api.errors import HttpMethodOnAPINotAllowedError
from ninja_extended.api.registry import APIOperationRegistry
from ninja_extended.api.router import ExtendedRouter

if TYPE_CHECKING:
    pass  # noqa: TCH005

__all__ = ["NinjaAPI"]

_E = TypeVar("_E", bound=Exception)
Exc = _E | type[_E]
ExcHandler = Callable[[HttpRequest, Exc[_E]], HttpResponse]


class ExtendedNinjaAPI(NinjaAPI):
    """Extended Ninja API."""

    def __init__(  # noqa: PLR0913
        self,
        title: str,
        version: str,
        description: str,
        *,
        openapi_url: str | None = "/openapi.json",
        docs: DocsBase = Swagger(),  # noqa: B008
        docs_url: str | None = "/docs",
        docs_decorator: Callable[[TCallable], TCallable] | None = None,
        servers: list[DictStrAny] | None = None,
        urls_namespace: str | None = None,
        csrf: bool = False,
        auth: Sequence[Callable] | Callable | NOT_SET_TYPE | None = NOT_SET,
        throttle: BaseThrottle | list[BaseThrottle] | NOT_SET_TYPE = NOT_SET,
        renderer: BaseRenderer | None = None,
        parser: Parser | None = None,
        default_router: ExtendedRouter | None = None,
        openapi_extra: dict[str, Any] | None = None,
    ):
        APIOperationRegistry.register_api(api=self)

        self.title = title
        self.version = version
        self.description = description
        self.openapi_url = openapi_url
        self.docs = docs
        self.docs_url = docs_url
        self.docs_decorator = docs_decorator
        self.servers = servers or []
        self.urls_namespace = urls_namespace or f"api-{self.version}"
        self.csrf = csrf  # TODO: Check if used or at least throw Deprecation warning
        if self.csrf:
            warnings.warn(
                "csrf argument is deprecated, auth is handling csrf automatically now",
                DeprecationWarning,
                stacklevel=2,
            )
        self.renderer = renderer or JSONRenderer()
        self.parser = parser or Parser()
        self.openapi_extra = openapi_extra or {}

        self._exception_handlers: dict[Exc, ExcHandler] = {}
        self.set_default_exception_handlers()

        self.auth: Sequence[Callable] | NOT_SET_TYPE | None

        if callable(auth):
            self.auth = [auth]
        else:
            self.auth = auth

        self.throttle = throttle

        self._routers: list[tuple[str, ExtendedRouter]] = []
        self.default_router = default_router or ExtendedRouter(tags=["default"])
        self.add_router("", self.default_router)

    def get(  # noqa: PLR0913
        self,
        path: str,
        operation_id: str,
        summary: str,
        description: str,
        tags: list[str],
        *,
        auth: Any = NOT_SET,
        throttle: BaseThrottle | list[BaseThrottle] | NOT_SET_TYPE = NOT_SET,
        response: Any = NOT_SET,
        deprecated: bool | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        url_name: str | None = None,
        include_in_schema: bool = True,
        openapi_extra: dict[str, Any] | None = None,
    ) -> Callable[[TCallable], TCallable]:
        """GET operation decorator."""

        raise HttpMethodOnAPINotAllowedError(method="GET")

    def post(  # noqa: PLR0913
        self,
        path: str,
        operation_id: str,
        summary: str,
        description: str,
        tags: list[str],
        *,
        auth: Any = NOT_SET,
        throttle: BaseThrottle | list[BaseThrottle] | NOT_SET_TYPE = NOT_SET,
        response: Any = NOT_SET,
        deprecated: bool | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        url_name: str | None = None,
        include_in_schema: bool = True,
        openapi_extra: dict[str, Any] | None = None,
    ) -> Callable[[TCallable], TCallable]:
        """POST operation decorator."""

        raise HttpMethodOnAPINotAllowedError(method="POST")

    def delete(  # noqa: PLR0913
        self,
        path: str,
        operation_id: str,
        summary: str,
        description: str,
        tags: list[str],
        *,
        auth: Any = NOT_SET,
        throttle: BaseThrottle | list[BaseThrottle] | NOT_SET_TYPE = NOT_SET,
        response: Any = NOT_SET,
        deprecated: bool | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        url_name: str | None = None,
        include_in_schema: bool = True,
        openapi_extra: dict[str, Any] | None = None,
    ) -> Callable[[TCallable], TCallable]:
        """DELETE operation decorator."""

        raise HttpMethodOnAPINotAllowedError(method="DELETE")

    def patch(  # noqa: PLR0913
        self,
        path: str,
        operation_id: str,
        summary: str,
        description: str,
        tags: list[str],
        *,
        auth: Any = NOT_SET,
        throttle: BaseThrottle | list[BaseThrottle] | NOT_SET_TYPE = NOT_SET,
        response: Any = NOT_SET,
        deprecated: bool | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        url_name: str | None = None,
        include_in_schema: bool = True,
        openapi_extra: dict[str, Any] | None = None,
    ) -> Callable[[TCallable], TCallable]:
        """PATCH operation decorator."""

        raise HttpMethodOnAPINotAllowedError(method="PATCH")

    def put(  # noqa: PLR0913
        self,
        path: str,
        operation_id: str,
        summary: str,
        description: str,
        tags: list[str],
        *,
        auth: Any = NOT_SET,
        throttle: BaseThrottle | list[BaseThrottle] | NOT_SET_TYPE = NOT_SET,
        response: Any = NOT_SET,
        deprecated: bool | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        url_name: str | None = None,
        include_in_schema: bool = True,
        openapi_extra: dict[str, Any] | None = None,
    ) -> Callable[[TCallable], TCallable]:
        """PUT operation decorator."""

        raise HttpMethodOnAPINotAllowedError(method="PUT")

    def add_router(  # noqa: PLR0913
        self,
        prefix: str,
        router: ExtendedRouter | str,
        *,
        auth: Any = NOT_SET,
        throttle: BaseThrottle | list[BaseThrottle] | NOT_SET_TYPE = NOT_SET,
        tags: list[str] | None = None,
        parent_router: ExtendedRouter | None = None,
    ) -> None:
        """Add router."""

        APIOperationRegistry.register_routers_operation_ids(api=self, router=router)

        super().add_router(
            prefix=prefix,
            router=router,
            auth=auth,
            throttle=throttle,
            tags=tags,
            parent_router=parent_router,
        )
