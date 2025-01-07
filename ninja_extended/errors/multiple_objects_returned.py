"""Module error.not_found."""

from decimal import Decimal
from typing import Literal

from pydantic import Field, create_model

from ninja_extended.errors.base import APIError
from ninja_extended.utils import (
    camel_to_kebap,
    convert_value_to_detail_string,
    pluralize,
)


class MultipleObjectsReturnedError(APIError):
    """Base multiple objects returned error class."""

    resource_name: str
    status: int = 422

    def __init__(
        self,
        fields: dict[str, bool | Decimal | float | int | str | None],
    ):
        """Initialize a MultipleObjectsReturnedError."""

        error_type = f"errors/{camel_to_kebap(value=pluralize(value=self.resource_name))}/multiple-objects-returned"
        title = f"Multiple {self.resource_name} objects returned."
        fields_string = ",".join([f"{key}={convert_value_to_detail_string(value)}" for key, value in fields.items()])
        detail = f"Multiple {self.resource_name} objects with ({fields_string}) returned."

        super().__init__(type=error_type, title=title, detail=detail)

        self.fields = fields

    def to_dict(self):
        """Serialize the MultipleObjectsReturnedError."""

        base_dict = super().to_dict()
        base_dict.update({"fields": self.fields})

        return base_dict

    @classmethod
    def schema(cls):
        """Return the schema for the error.

        Returns:
            type[BaseModel]: The schema.
        """

        model_name = f"{cls.resource_name}MultipleObjectsReturnedErrorResponse"
        error_type = f"errors/{camel_to_kebap(value=pluralize(value=cls.resource_name))}/multiple-objects-returned"
        title = f"Multiple {cls.resource_name} objects returned."

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
                str,
                Field(description=f"The detail of the {model_name}."),
            ),
            fields=(
                dict[str, bool | Decimal | float | int | str | None],
                Field(description=f"The fields of the {model_name}."),
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
