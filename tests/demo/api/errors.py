"""Module tests.demo.api.errors."""

from ninja_extended.errors import (
    CheckConstraintError,
    MultipleObjectsReturnedError,
    NotFoundError,
    NotNullConstraintError,
    ProtectedError,
    UniqueConstraintError,
)


class ResourceCheckConstraintError(CheckConstraintError):
    resource = "Resource"


class ResourceMultipleObjectsReturnedError(MultipleObjectsReturnedError):
    resource = "Resource"


class ResourceNotFoundError(NotFoundError):
    resource = "Resource"


class ResourceNotNullConstraintError(NotNullConstraintError):
    resource = "Resource"


class ResourceProtectedError(ProtectedError):
    resource = "Resource"


class ResourceUniqueConstraintError(UniqueConstraintError):
    resource = "Resource"
