"""Module fields.base."""

from typing import Any

from pydantic import BaseModel, Field
from pydantic_core import PydanticUndefined


class BaseFieldValues(BaseModel):
    """Base schema for fields."""

    description: str = Field(
        description="The description of a field.",
        strict=True,
        min_length=3,
    )
    strict: bool | None = Field(
        description="Whether to validate the value in strict mode.",
        default=True,
        strict=True,
    )


def BaseField(field_values: BaseFieldValues, default: Any = PydanticUndefined) -> Any:  # noqa: N802
    """Wrap pydantics Field function.

    Args:
        field_values (BaseFieldValues): The field value definition.
        default (Any, optional): The default value. Defaults to PydanticUndefined.

    Returns:
        Any: The return value of pydantics Field function.
    """

    return Field(**field_values.model_dump(), default=default)
