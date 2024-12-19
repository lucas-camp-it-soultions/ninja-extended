"""Module fields.datetime."""

from datetime import datetime
from typing import Any

from pydantic import Field as PydanticField
from pydantic_core import PydanticUndefined, PydanticUndefinedType

from .base import BaseField, BaseFieldValues


class DatetimeFieldValues(BaseFieldValues):
    """Schema for datetime fields."""

    gt: datetime | None = PydanticField(
        description="The value must be greater than this.",
        default=None,
        strict=True,
    )
    ge: datetime | None = PydanticField(
        description="The value must be greater than or equal to this.",
        default=None,
        strict=True,
    )
    lt: datetime | None = PydanticField(
        description="The value must be less than this.",
        default=None,
        strict=True,
    )
    le: datetime | None = PydanticField(
        description="The value must be less than or equal to this.",
        default=None,
        strict=True,
    )


def DatetimeField(  # noqa: N802
    field_values: DatetimeFieldValues,
    default: datetime | None | PydanticUndefinedType = PydanticUndefined,
) -> Any:
    """Wrap pydantics Field function for datetime fields.

    Args:
        field_values (DatetimeFieldValues): The field value definition.
        default (datetime | None | PydanticUndefinedType, optional): The default value. Defaults to PydanticUndefined.

    Returns:
        Any: The return value of pydantics Field function.
    """

    return BaseField(field_values=field_values, default=default)
