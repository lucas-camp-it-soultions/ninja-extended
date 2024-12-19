"""Module api.router."""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from ninja import Router
from ninja.constants import NOT_SET, NOT_SET_TYPE
from ninja.throttling import BaseThrottle
from ninja.types import TCallable

from ninja_extended.api.operation import ExtendedPathView
from ninja_extended.api.registry import RouterOperationRegistry

if TYPE_CHECKING:
    from ninja_extended.api import ExtendedNinjaAPI


class ExtendedRouter(Router):
    """Extended Router."""

    def __init__(
        self,
        *,
        auth: Any = NOT_SET,
        throttle: BaseThrottle | list[BaseThrottle] | NOT_SET_TYPE = NOT_SET,
        tags: list[str] | None = None,
    ) -> None:
        """Initialize an ExtendedRouter."""

        RouterOperationRegistry.register_router(router=self)

        self.api: ExtendedNinjaAPI | None = None
        self.auth = auth
        self.throttle = throttle
        self.tags = tags
        self.path_operations: dict[str, ExtendedPathView] = {}
        self._routers: list[tuple[str, ExtendedRouter]] = []

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

        return self.api_operation(
            ["GET"],
            path=path,
            operation_id=operation_id,
            summary=summary,
            description=description,
            tags=tags,
            auth=auth,
            throttle=throttle,
            response=response,
            deprecated=deprecated,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            url_name=url_name,
            include_in_schema=include_in_schema,
            openapi_extra=openapi_extra,
        )

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

        return self.api_operation(
            ["POST"],
            path=path,
            operation_id=operation_id,
            summary=summary,
            description=description,
            tags=tags,
            auth=auth,
            throttle=throttle,
            response=response,
            deprecated=deprecated,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            url_name=url_name,
            include_in_schema=include_in_schema,
            openapi_extra=openapi_extra,
        )

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

        return self.api_operation(
            ["DELETE"],
            path=path,
            operation_id=operation_id,
            summary=summary,
            description=description,
            tags=tags,
            auth=auth,
            throttle=throttle,
            response=response,
            deprecated=deprecated,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            url_name=url_name,
            include_in_schema=include_in_schema,
            openapi_extra=openapi_extra,
        )

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

        return self.api_operation(
            ["PATCH"],
            path=path,
            operation_id=operation_id,
            summary=summary,
            description=description,
            tags=tags,
            auth=auth,
            throttle=throttle,
            response=response,
            deprecated=deprecated,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            url_name=url_name,
            include_in_schema=include_in_schema,
            openapi_extra=openapi_extra,
        )

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

        return self.api_operation(
            ["PUT"],
            path=path,
            operation_id=operation_id,
            summary=summary,
            description=description,
            tags=tags,
            auth=auth,
            throttle=throttle,
            response=response,
            deprecated=deprecated,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            url_name=url_name,
            include_in_schema=include_in_schema,
            openapi_extra=openapi_extra,
        )

    def api_operation(  # noqa: PLR0913
        self,
        methods: list[str],
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
        """Add generic HTTP method handler."""

        RouterOperationRegistry.register_operation_id(router=self, operation_id=operation_id)

        def decorator(view_func: TCallable) -> TCallable:
            self.add_api_operation(
                path=path,
                operation_id=operation_id,
                summary=summary,
                description=description,
                tags=tags,
                methods=methods,
                view_func=view_func,
                auth=auth,
                throttle=throttle,
                response=response,
                deprecated=deprecated,
                by_alias=by_alias,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                url_name=url_name,
                include_in_schema=include_in_schema,
                openapi_extra=openapi_extra,
            )
            return view_func

        return decorator

    def add_api_operation(  # noqa: PLR0913
        self,
        path: str,
        operation_id: str,
        summary: str,
        description: str,
        tags: list[str],
        methods: list[str],
        view_func: Callable,
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
    ) -> None:
        """Add an API operation."""

        if path not in self.path_operations:
            path_view = ExtendedPathView()
            self.path_operations[path] = path_view
        else:
            path_view = self.path_operations[path]
        path_view.add_operation(
            path=path,
            operation_id=operation_id,
            summary=summary,
            description=description,
            tags=tags,
            methods=methods,
            view_func=view_func,
            auth=auth,
            throttle=throttle,
            response=response,
            deprecated=deprecated,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            url_name=url_name,
            include_in_schema=include_in_schema,
            openapi_extra=openapi_extra,
        )
        if self.api:
            path_view.set_api_instance(self.api, self)
