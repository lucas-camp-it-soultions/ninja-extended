"""Module pagination.page_number_page_size."""

from math import ceil
from typing import Any
from urllib.parse import urlparse

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Field, Schema
from ninja.conf import settings
from ninja.errors import ValidationError
from ninja.pagination import AsyncPaginationBase


class PageNumberPageSizePagination(AsyncPaginationBase):
    """Pagination with page number and page size."""

    class Input(Schema):
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
        pagination: Input,
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
        pagination: Input,
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
