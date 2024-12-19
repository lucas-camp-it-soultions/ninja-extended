"""Module errors.base."""

from pydantic import BaseModel


class APIError(Exception):
    """Base error class."""

    status: int

    def __init__(self, type: str, title: str, detail: str | None):  # noqa: A002
        """Initialize an APIError."""

        super().__init__()

        self.type = type
        self.title = title
        self.detail = detail

    def to_dict(self):
        """Serialize the APIError."""

        return {
            "type": self.type,
            "status": self.status,
            "title": self.title,
            "detail": self.detail,
        }

    @classmethod
    def schema(cls) -> type[BaseModel]:
        """Return the schema for the error.

        Returns:
            type[BaseModel]: The schema.
        """

        raise NotImplementedError("The method 'schema' must be implemented.")  # noqa: EM101


class APIErrorResponse(BaseModel):
    """Schema for base error class."""

    type: str
    status: int
    title: str
    detail: str | None = None
    path: str
    opertaion_id: str
