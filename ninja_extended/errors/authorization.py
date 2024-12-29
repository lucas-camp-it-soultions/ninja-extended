"""Module error.authorization."""

from typing import Literal

from pydantic import Field, create_model

from ninja_extended.errors.base import APIError


class AuthorizationError(APIError):
    """Authorization error class."""

    resource_name: str
    status: int = 403

    def __init__(
        self,
        operation: str,
    ):
        """Initialize a AuthorizationError."""

        error_type = "errors/auth/authorization"
        title = "Unsufficient permissions for the operation."
        detail = f"Unsufficient permissions for the operation '{operation}'."

        super().__init__(type=error_type, title=title, detail=detail)

        self.operation=operation

    def to_dict(self):
        """Serialize the AuthorizationError."""

        base_dict = super().to_dict()
        base_dict.update({"operation": self.operation})

        return base_dict

    @classmethod
    def schema(cls):
        """Return the schema for the error.

        Returns:
            type[BaseModel]: The schema.
        """

        model_name = "AuthorizationErrorResponse"
        error_type = "errors/auth/authorization"
        title = "Unsufficient permissions for the operation."

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
            operation=(
                str,
                Field(description=f"The operation of the {model_name}."),
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
