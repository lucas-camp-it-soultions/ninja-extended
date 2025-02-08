"""Module fields.string."""

from re import Pattern
from typing import Any

from pydantic import Field as PydanticField
from pydantic_core import PydanticUndefined, PydanticUndefinedType

from .base import BaseField, BaseFieldValues


class StringFieldValues(BaseFieldValues):
    """Schema for string fields."""

    min_length: int | None = PydanticField(
        description="The minimum length of the string.",
        default=None,
        strict=True,
    )
    max_length: int | None = PydanticField(
        description="The maximum length of the string.",
        default=None,
        strict=True,
    )
    pattern: str | Pattern[str] | None = PydanticField(
        description="A regex pattern to validate the string against.",
        default=None,
    )


def StringField(  # noqa: N802
    field_values: StringFieldValues,
    default: str | None | PydanticUndefinedType = PydanticUndefined,
) -> Any:
    """Wrap pydantics Field function for string fields.

    Args:
        field_values (StringFieldValues): The field value definition.
        default (str | None | PydanticUndefinedType, optional): The default value. Defaults to PydanticUndefined.

    Returns:
        Any: The return value of pydantics Field function.
    """

    return BaseField(field_values=field_values, default=default)
