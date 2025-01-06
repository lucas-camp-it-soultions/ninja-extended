"""Module error.not_found."""

from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, create_model

from ninja_extended.errors.base import APIError
from ninja_extended.utils import camel_to_pascal, snake_to_camel, snake_to_kebap


class ValidationErrorDetail(BaseModel):
    """Schema for Ninja ValidationError."""

    type: str
    loc: tuple[str | int, ...]
    msg: str
    ctx: dict[str, Any] | None = Field(default=None)


class ValidationError(APIError):
    """Base not found error class."""

    router_prefix: str | None = None
    operation_id: str
    status: int = 422

    def __init__(self, errors: list[ValidationErrorDetail]):
        """Initialize a ValidationError."""

        if self.router_prefix is not None:
            error_type = f"errors/{self.router_prefix}/{snake_to_kebap(value=self.operation_id)}/validation"
        else:
            error_type = f"errors/{snake_to_kebap(value=self.operation_id)}/validation"
        title = f"Validation for operation {self.operation_id} failed."
        detail = f"Validation for operation {self.operation_id} failed."

        super().__init__(type=error_type, title=title, detail=detail)

        self.errors = errors

    def to_dict(self):
        """Serialize the NotFoundError."""

        base_dict = super().to_dict()
        base_dict.update({"errors": self.errors})

        return base_dict

    @classmethod
    def schema(cls):
        """Return the schema for the error.

        Returns:
            type[BaseModel]: The schema.
        """

        model_name = f"{camel_to_pascal(value=snake_to_camel(value=cls.operation_id))}ValidationErrorResponse"

        if cls.router_prefix is not None:
            error_type = f"errors/{cls.router_prefix}/{snake_to_kebap(value=cls.operation_id)}/validation"
        else:
            error_type = f"errors/{snake_to_kebap(value=cls.operation_id)}/validation"
        title = f"Validation for operation {cls.operation_id} failed."
        detail = f"Validation for operation {cls.operation_id} failed."

        return create_model(
            model_name,
            type=(
                Literal[error_type],
                Field(description=f"The type of the {model_name}."),
            ),
            status=(
                Literal[cls.status],
                Field(description=f"The status of the {model_name}."),
            ),
            title=(
                Literal[title],
                Field(description=f"The title of the {model_name}."),
            ),
            detail=(
                Literal[detail],
                Field(description=f"The detail of the {model_name}."),
            ),
            errors=(
                list[ValidationErrorDetail],
                Field(description=f"The error details of the {model_name}."),
            ),
            path=(
                str,
                Field(description=f"The path of the {model_name}."),
            ),
            operation_id=(
                str,
                Field(description=f"The operation id of the {model_name}."),
            ),
        )


def validation_error_factory(router_prefix: str | None, operation_id: str) -> type[APIError]:
    """Create a ValidationError dynamically.

    Args:
        router_prefix (str | None): The router prefix.
        operation_id (str): The operation id.

    Returns:
        type[APIError]: The dynamic ValidationError type.
    """

    return type(
        f"{camel_to_pascal(value=snake_to_camel(value=operation_id))}ValidationError",
        (ValidationError,),
        {"router_prefix": router_prefix, "operation_id": operation_id},
    )


def discriminate_validation_errors(error_types: list[type[APIError]]):
    """Build a discriminated union of error type.

    Args:
        error_types (list[type[APIError]]): The error types.

    Raises:
        RuntimeError: If no error types are provided.

    Returns:
        _type_: The disciminated union of error types.
    """

    error_message_no_types = "At least one error type must be provided"

    if len(error_types) == 0:
        raise RuntimeError(error_message_no_types)

    schema = error_types[0].schema()

    if len(error_types) == 1:
        return schema

    for error_type in error_types[1:]:
        schema |= error_type.schema()

    return Annotated[schema, Field(discriminator="type")]
