"""Module pagination.page_number_page_size."""

from collections.abc import AsyncGenerator, Callable
from functools import partial, wraps
from math import ceil
from typing import Any
from urllib.parse import urlparse

import ninja.pagination
from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Field, Schema
from ninja.conf import settings
from ninja.errors import ConfigError, ValidationError
from ninja.pagination import AsyncPaginationBase, PaginationBase, make_response_paginated
from ninja.utils import (
    contribute_operation_args,
    contribute_operation_callback,
    is_async_callable,
)


def _inject_page_number_page_size_pagination(
    func: Callable,
    paginator_class: type[PaginationBase | AsyncPaginationBase],
    **paginator_params: Any,
) -> Callable:
    paginator = paginator_class(**paginator_params)
    if is_async_callable(func):
        if not hasattr(paginator, "apaginate_queryset"):
            raise ConfigError("Pagination class not configured for async requests")  # noqa: EM101

        @wraps(func)
        async def view_with_pagination(request: HttpRequest, **kwargs: Any) -> Any:
            pagination_params = kwargs.pop("ninja_pagination")
            if paginator.pass_parameter:
                kwargs[paginator.pass_parameter] = pagination_params

            items = await func(request, **kwargs)

            result = await paginator.apaginate_queryset(items, pagination=pagination_params, request=request, **kwargs)

            async def evaluate(results: list | QuerySet) -> AsyncGenerator:
                for result in results:
                    yield result

            if paginator.Output:
                result[paginator.items_attribute] = [
                    result async for result in evaluate(result[paginator.items_attribute])
                ]
            return result

    else:

        @wraps(func)
        def view_with_pagination(request: HttpRequest, **kwargs: Any) -> Any:
            pagination_params = kwargs.pop("ninja_pagination")
            if paginator.pass_parameter:
                kwargs[paginator.pass_parameter] = pagination_params

            items = func(request, **kwargs)

            result = paginator.paginate_queryset(items, pagination=pagination_params, request=request, **kwargs)
            if paginator.Output:
                result[paginator.items_attribute] = list(result[paginator.items_attribute])
                # ^ forcing queryset evaluation #TODO: check why pydantic did not do it here
            return result

    contribute_operation_args(
        view_with_pagination,
        "ninja_pagination",
        paginator.PageNumberPageSizePaginationInput,
        paginator.InputSource,
    )

    if paginator.Output:
        contribute_operation_callback(
            view_with_pagination,
            partial(make_response_paginated, paginator),
        )

    return view_with_pagination


ninja.pagination._inject_pagination = _inject_page_number_page_size_pagination  # noqa: SLF001


class PageNumberPageSizePagination(AsyncPaginationBase):
    """Pagination with page number and page size."""

    class PageNumberPageSizePaginationInput(Schema):
        """Input for PageNumberPagination."""

        page: int = Field(1, ge=1)
        page_size: int = Field(settings.PAGINATION_PER_PAGE, ge=1)

    class Output(Schema):
        """Output for PageNumberPagination."""

        count: int
        current_page: int
        pages: int
        previous_page: int | None
        next_page: int | None
        previous_url: str | None
        next_url: str | None

    def __init__(self, **kwargs: Any) -> None:
        """Initialize a PageNumberPageSizePagination."""

        super().__init__(**kwargs)

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: PageNumberPageSizePaginationInput,
        request: HttpRequest,
        **params: Any,  # noqa: ARG002
    ) -> Any:
        """Paginate the queryset."""

        offset = (pagination.page - 1) * pagination.page_size
        count = self._items_count(queryset)
        pages = ceil(count / pagination.page_size)

        if pagination.page > pages:
            raise ValidationError(
                errors=[
                    {
                        "type": "less_than_equal",
                        "loc": ("query", "page"),
                        "msg": f"Input should be less than or equal to {pages}",
                        "ctx": {
                            "le": pages,
                        },
                    }
                ]
            )

        if count == 0:
            return {
                "count": 0,
                "current_page": 0,
                "pages": 0,
                "previous_page": None,
                "next_page": None,
                "previous_url": None,
                "next_url": None,
                "items": [],
            }

        next_page, previous_page = None, None
        next_url, previous_url = None, None

        if pagination.page > 1:
            previous_page = pagination.page - 1
            previous_url = request.build_absolute_uri(
                f"{urlparse(request.path).path}?page_size={pagination.page_size}&page={previous_page}"
            )
        if offset + pagination.page_size < count:
            next_page = pagination.page + 1
            next_url = request.build_absolute_uri(
                f"{urlparse(request.path).path}?page_size={pagination.page_size}&page={next_page}"
            )

        return {
            "count": count,
            "current_page": pagination.page,
            "pages": pages,
            "previous_page": previous_page,
            "next_page": next_page,
            "previous_url": previous_url,
            "next_url": next_url,
            "items": queryset[offset : offset + pagination.page_size],
        }

    def apaginate_queryset(
        self,
        queryset: QuerySet,
        pagination: PageNumberPageSizePaginationInput,
        request: HttpRequest,
        **params: Any,  # noqa: ARG002
    ) -> Any:
        """Paginate the queryset."""

        offset = (pagination.page - 1) * pagination.page_size
        count = self._aitems_count(queryset)
        pages = ceil(count / pagination.page_size)

        if pagination.page > pages:
            raise ValidationError(
                errors=[
                    {
                        "type": "less_than_equal",
                        "loc": ("query", "page"),
                        "msg": f"Input should be less than or equal to {pages}",
                        "ctx": {
                            "le": pages,
                        },
                    }
                ]
            )

        if count == 0:
            return {
                "count": 0,
                "current_page": 0,
                "pages": 0,
                "previous_page": None,
                "next_page": None,
                "previous_url": None,
                "next_url": None,
                "items": [],
            }

        next_page, previous_page = None, None
        next_url, previous_url = None, None

        if pagination.page > 1:
            previous_page = pagination.page - 1
            previous_url = request.build_absolute_uri(
                f"{urlparse(request.path).path}?page_size={pagination.page_size}&page={previous_page}"
            )
        if offset + pagination.page_size < count:
            next_page = pagination.page + 1
            next_url = request.build_absolute_uri(
                f"{urlparse(request.path).path}?page_size={pagination.page_size}&page={next_page}"
            )

        return {
            "count": count,
            "current_page": pagination.page,
            "pages": pages,
            "previous_page": previous_page,
            "next_page": next_page,
            "previous_url": previous_url,
            "next_url": next_url,
            "items": queryset[offset : offset + pagination.page_size],
        }
