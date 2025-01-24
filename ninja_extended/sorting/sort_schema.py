"""Module sorting.sort_schema."""

from copy import copy
from enum import Enum, EnumMeta, unique
from types import DynamicClassAttribute
from typing import TypeVar

from django.db.models import QuerySet
from ninja import Schema

T = TypeVar("T", bound=QuerySet)


class SortEnumMeta(EnumMeta):
    """Meta class for SortEnum."""

    def __new__(metacls, cls, bases, classdict, **kwds):  # noqa: N804
        """Create a new SortEnum."""

        member_names = copy(classdict._member_names)  # noqa: SLF001
        fields = []

        for member_name in member_names:
            value = classdict[member_name]
            del classdict[member_name]
            classdict._member_names.remove(member_name)  # noqa: SLF001

            key_asc = f"{member_name}_asc"
            field_asc = value
            key_desc = f"{member_name}_desc"
            field_desc = f"-{value}"

            classdict[key_asc] = key_asc
            classdict[key_desc] = key_desc

            fields.append(field_asc)
            fields.append(field_desc)

        cls = super().__new__(metacls, cls, bases, classdict, **kwds)

        for member, field in zip(cls.__members__.values(), fields):  # noqa: B905
            member._field_ = field

        return unique(cls)

    @property
    def names(cls):
        """Get all names."""

        empty = ["__empty__"] if hasattr(cls, "__empty__") else []
        return empty + [member.name for member in cls]

    @property
    def items(cls):
        """Get all items."""

        empty = [(None, cls.__empty__)] if hasattr(cls, "__empty__") else []
        return empty + [(member.value, member.field) for member in cls]

    @property
    def fields(cls):
        """Get all fields."""

        return [field for _, field in cls.items]

    @property
    def values(cls):
        """Get all values."""

        return [value for value, _ in cls.items]


class SortEnum(Enum, metaclass=SortEnumMeta):
    """Enum for sorting."""

    def __repr__(self):
        """Get the representation of the SortEnum."""

        return f"{self.__class__.__qualname__}.{self._name_}"

    def __str__(self):
        """Get the string representation of the SortEnum."""

        return str(self.value)

    @DynamicClassAttribute
    def field(self):
        """Get the field."""

        return self._field_


class SortableFieldsEnum(str, SortEnum):
    """Enum for sorting fields."""


class SortSchema(Schema):
    """Schema for sorting."""

    ordering: list[SortableFieldsEnum] | None

    def sort(self, queryset: T) -> T:
        """Sort the queryset."""

        ordering = [o._field_ for o in self.ordering] if self.ordering is not None else None

        return queryset.order_by(*ordering)
