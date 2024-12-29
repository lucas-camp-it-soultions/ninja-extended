"""Module error.authentication."""

from typing import Literal

from pydantic import Field, create_model

from ninja_extended.errors.base import APIError


class AuthenticationError(APIError):
    """Authentication error class."""

    resource_name: str
    status: int = 401

    def __init__(
        self,
    ):
        """Initialize a AuthenticationError."""

        error_type = "errors/auth/authentication"
        title = "Not authenticated."
        detail = "Not authenticated."

        super().__init__(type=error_type, title=title, detail=detail)

    @classmethod
    def schema(cls):
        """Return the schema for the error.

        Returns:
            type[BaseModel]: The schema.
        """

        model_name = "AuthenticationErrorResponse"
        error_type = "errors/auth/authentication"
        title = "Not authenticated."
        detail = "Not authenticated."

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
            path=(
                str,
                Field(description=f"The path of the {model_name}."),
            ),
            operation_id=(
                str,
                Field(description=f"The operation id of the {model_name}."),
            ),
        )
