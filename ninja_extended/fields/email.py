"""Module fields.email."""

from typing import Any

from pydantic_core import PydanticUndefined, PydanticUndefinedType

from .base import BaseField, BaseFieldValues


class EmailFieldValues(BaseFieldValues):
    """Schema for email fields."""


def EmailField(  # noqa: N802
    field_values: EmailFieldValues,
    default: str | None | PydanticUndefinedType = PydanticUndefined,
) -> Any:
    """Wrap pydantics Field function for email fields.

    Args:
        field_values (EmailFieldValues): The field value definition.
        default (str | None | PydanticUndefinedType, optional): The default value. Defaults to PydanticUndefined.

    Returns:
        Any: The return value of pydantics Field function.
    """

    return BaseField(field_values=field_values, default=default)
