"""Module fields.date."""

from datetime import date
from typing import Any

from pydantic import Field as PydanticField
from pydantic_core import PydanticUndefined, PydanticUndefinedType

from .base import BaseField, BaseFieldValues


class DateFieldValues(BaseFieldValues):
    """Schema for date fields."""

    gt: date | None = PydanticField(
        description="The value must be greater than this.",
        default=None,
        strict=True,
    )
    ge: date | None = PydanticField(
        description="The value must be greater than or equal to this.",
        default=None,
        strict=True,
    )
    lt: date | None = PydanticField(
        description="The value must be less than this.",
        default=None,
        strict=True,
    )
    le: date | None = PydanticField(
        description="The value must be less than or equal to this.",
        default=None,
        strict=True,
    )


def DateField(  # noqa: N802
    field_values: DateFieldValues,
    default: date | None | PydanticUndefinedType = PydanticUndefined,
) -> Any:
    """Wrap pydantics Field function for date fields.

    Args:
        field_values (DateFieldValues): The field value definition.
        default (date | None | PydanticUndefinedType, optional): The default value. Defaults to PydanticUndefined.

    Returns:
        Any: The return value of pydantics Field function.
    """

    return BaseField(field_values=field_values, default=default)
