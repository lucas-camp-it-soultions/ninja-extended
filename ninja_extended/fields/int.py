"""Module fields.email."""

from typing import Any

from pydantic import Field as PydanticField
from pydantic_core import PydanticUndefined, PydanticUndefinedType

from .base import BaseField, BaseFieldValues


class IntFieldValues(BaseFieldValues):
    """Schema for int fields."""

    gt: int | None = PydanticField(
        description="The value must be greater than this.",
        default=None,
        strict=True,
    )
    ge: int | None = PydanticField(
        description="The value must be greater than or equal to this.",
        default=None,
        strict=True,
    )
    lt: int | None = PydanticField(
        description="The value must be less than this.",
        default=None,
        strict=True,
    )
    le: int | None = PydanticField(
        description="The value must be less than or equal to this.",
        default=None,
        strict=True,
    )
    multiple_of: int | None = PydanticField(
        description="The value must be a multiple of this.",
        default=None,
        strict=True,
    )


def IntField(  # noqa: N802
    field_values: IntFieldValues,
    default: int | None | PydanticUndefinedType = PydanticUndefined,
) -> Any:
    """Wrap pydantics Field function for int fields.

    Args:
        field_values (IntFieldValues): The field value definition.
        default (int | None | PydanticUndefinedType, optional): The default value. Defaults to PydanticUndefined.

    Returns:
        Any: The return value of pydantics Field function.
    """

    return BaseField(field_values=field_values, default=default)
