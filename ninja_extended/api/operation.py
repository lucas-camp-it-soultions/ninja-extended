"""Module api.operation."""

from collections.abc import Callable, Sequence
from typing import Any

from django.http import HttpRequest
from django.http.response import HttpResponseBase
from ninja.constants import NOT_SET, NOT_SET_TYPE
from ninja.operation import Operation, PathView
from ninja.signature import is_async
from ninja.throttling import BaseThrottle


class ExtendedOperation(Operation):
    """Extended Operation."""

    def __init__(  # noqa: PLR0913
        self,
        path: str,
        operation_id: str,
        summary: str,
        description: str,
        tags: list[str],
        methods: list[str],
        view_func: Callable,
        *,
        auth: Sequence[Callable] | Callable | NOT_SET_TYPE | None = NOT_SET,
        throttle: BaseThrottle | list[BaseThrottle] | NOT_SET_TYPE = NOT_SET,
        response: Any = NOT_SET,
        deprecated: bool | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        include_in_schema: bool = True,
        url_name: str | None = None,
        openapi_extra: dict[str, Any] | None = None,
    ) -> None:
        """Initialize an ExtendedOperation.

        Args:
            path (str): The path.
            operation_id (str): The operation id.
            summary (str): The summary.
            description (str): The description.
            tags (list[str]): The tags.
            methods (list[str]): The HTTP methods.
            view_func (Callable): The handler function.
            auth (Sequence[Callable] | Callable | NOT_SET_TYPE | None, optional): The auth instance. Defaults to NOT_SET.
            throttle (BaseThrottle | list[BaseThrottle] | NOT_SET_TYPE, optional): The throttle instance. Defaults to NOT_SET.
            response (Any, optional): The response type. Defaults to NOT_SET.
            deprecated (bool | None, optional): If the operation is deprecated. Defaults to None.
            by_alias (bool, optional): Initialize the attributes by alias. Defaults to False.
            exclude_unset (bool, optional): Exclude attributes that are not set. Defaults to False.
            exclude_defaults (bool, optional): Exclude default attributes. Defaults to False.
            exclude_none (bool, optional): Exclude attributes that are None. Defaults to False.
            include_in_schema (bool, optional): Include the operation in the OpenAPI schema. Defaults to True.
            url_name (str | None, optional): The url name. Defaults to None.
            openapi_extra (dict[str, Any] | None, optional): Extras for the OpenAPI schema. Defaults to None.
        """
        super().__init__(
            path=path,
            methods=methods,
            view_func=view_func,
            auth=auth,
            throttle=throttle,
            response=response,
            operation_id=operation_id,
            summary=summary,
            description=description,
            tags=tags,
            deprecated=deprecated,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            include_in_schema=include_in_schema,
            url_name=url_name,
            openapi_extra=openapi_extra,
        )

        self.operation_id: str
        self.summary: str
        self.description: str
        self.tags: list[str]

    def run(self, request: HttpRequest, **kw: Any) -> HttpResponseBase:
        """Run the operation.

        Args:
            request (HttpRequest): The request.
            **kw: Additional keyword arguments.

        Returns:
            HttpResponseBase: The response.
        """

        request.operation_id = self.operation_id

        return super().run(request=request, **kw)


class ExtendedAsyncOperation(ExtendedOperation):
    """Extended Async Operation."""

    def __init__(  # noqa: PLR0913
        self,
        path: str,
        operation_id: str,
        summary: str,
        description: str,
        tags: list[str],
        methods: list[str],
        view_func: Callable,
        *,
        auth: Sequence[Callable] | Callable | NOT_SET_TYPE | None = NOT_SET,
        throttle: BaseThrottle | list[BaseThrottle] | NOT_SET_TYPE = NOT_SET,
        response: Any = NOT_SET,
        deprecated: bool | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        include_in_schema: bool = True,
        url_name: str | None = None,
        openapi_extra: dict[str, Any] | None = None,
    ) -> None:
        """Initialize an ExtendedOperation.

        Args:
            path (str): The path.
            operation_id (str): The operation id.
            summary (str): The summary.
            description (str): The description.
            tags (list[str]): The tags.
            methods (list[str]): The HTTP methods.
            view_func (Callable): The handler function.
            auth (Sequence[Callable] | Callable | NOT_SET_TYPE | None, optional): The auth instance. Defaults to NOT_SET.
            throttle (BaseThrottle | list[BaseThrottle] | NOT_SET_TYPE, optional): The throttle instance. Defaults to NOT_SET.
            response (Any, optional): The response type. Defaults to NOT_SET.
            deprecated (bool | None, optional): If the operation is deprecated. Defaults to None.
            by_alias (bool, optional): Initialize the attributes by alias. Defaults to False.
            exclude_unset (bool, optional): Exclude attributes that are not set. Defaults to False.
            exclude_defaults (bool, optional): Exclude default attributes. Defaults to False.
            exclude_none (bool, optional): Exclude attributes that are None. Defaults to False.
            include_in_schema (bool, optional): Include the operation in the OpenAPI schema. Defaults to True.
            url_name (str | None, optional): The url name. Defaults to None.
            openapi_extra (dict[str, Any] | None, optional): Extras for the OpenAPI schema. Defaults to None.
        """
        super().__init__(
            path=path,
            methods=methods,
            view_func=view_func,
            auth=auth,
            throttle=throttle,
            response=response,
            operation_id=operation_id,
            summary=summary,
            description=description,
            tags=tags,
            deprecated=deprecated,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            include_in_schema=include_in_schema,
            url_name=url_name,
            openapi_extra=openapi_extra,
        )

        self.is_async = True

    async def run(self, request: HttpRequest, **kw: Any) -> HttpResponseBase:
        """Run the operation.

        Args:
            request (HttpRequest): The request.
            **kw: Additional keyword arguments.

        Returns:
            HttpResponseBase: The response.
        """

        request.operation_id = self.operation_id

        return super().run(request, **kw)


class ExtendedPathView(PathView):
    """Extended PathView."""

    def __init__(self) -> None:
        """Initialize an ExtendedPathView."""

        super().__init__()

        self.operations: list[ExtendedOperation] = []

    def add_operation(  # noqa: PLR0913
        self,
        path: str,
        operation_id: str,
        summary: str,
        description: str,
        tags: list[str],
        methods: list[str],
        view_func: Callable,
        *,
        auth: Sequence[Callable] | Callable | NOT_SET_TYPE | None = NOT_SET,
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
    ) -> Operation:
        """Add an operation.

        Args:
            path (str): The path.
            operation_id (str): The operation id.
            summary (str): The summary.
            description (str): The description.
            tags (list[str]): The tags.
            methods (list[str]): The HTTP methods.
            view_func (Callable): The handler function.
            auth (Sequence[Callable] | Callable | NOT_SET_TYPE | None, optional): The auth instance. Defaults to NOT_SET.
            throttle (BaseThrottle | list[BaseThrottle] | NOT_SET_TYPE, optional): The thorttle instance. Defaults to NOT_SET.
            response (Any, optional): The response model. Defaults to NOT_SET.
            deprecated (bool | None, optional): If the operation is deprecated. Defaults to None.
            by_alias (bool, optional): Initialize the attributes by alias. Defaults to False.
            exclude_unset (bool, optional): Exclude attributes that are not set. Defaults to False.
            exclude_defaults (bool, optional): Exclude default attributes. Defaults to False.
            exclude_none (bool, optional): Exclude attributes that are None. Defaults to False.
            url_name (str | None, optional): The url name. Defaults to None.
            include_in_schema (bool, optional): Include the operation in the OpenAPI schema. Defaults to True.
            openapi_extra (dict[str, Any] | None, optional): Extras for the OpenAPI schema. Defaults to None.

        Returns:
            Operation: _description_
        """
        if url_name:
            self.url_name = url_name

        operation_class = ExtendedOperation
        if is_async(view_func):
            self.is_async = True
            operation_class = ExtendedAsyncOperation

        operation = operation_class(
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
            include_in_schema=include_in_schema,
            url_name=url_name,
            openapi_extra=openapi_extra,
        )

        self.operations.append(operation)
        view_func._ninja_operation = operation  # noqa: SLF001
        return operation
