"""Module fields.bool."""

from typing import Any

from pydantic_core import PydanticUndefined, PydanticUndefinedType

from .base import BaseField, BaseFieldValues


class BoolFieldValues(BaseFieldValues):
    """Schema for bool fields."""


def BoolField(  # noqa: N802
    field_values: BoolFieldValues,
    default: bool | None | PydanticUndefinedType = PydanticUndefined,
) -> Any:
    """Wrap pydantics Field function for bool fields.

    Args:
        field_values (BoolFieldValues): The field value definition.
        default (bool | None | PydanticUndefinedType, optional): The default value. Defaults to PydanticUndefined.

    Returns:
        Any: The return value of pydantics Field function.
    """
    return BaseField(field_values=field_values, default=default)
