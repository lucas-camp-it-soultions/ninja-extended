"""Module errors."""

# ruff: noqa: F401

from ninja_extended.errors.authentication import AuthenticationError
from ninja_extended.errors.authorization import AuthorizationError
from ninja_extended.errors.base import APIError, APIErrorResponse, register_error_handler
from ninja_extended.errors.check_constraint import CheckConstraintError, check_constraint_error_factory
from ninja_extended.errors.csrf import CSRFError
from ninja_extended.errors.integrity import handle_integrity_error
from ninja_extended.errors.multiple_objects_returned import (
    MultipleObjectsReturnedError,
    multiple_objects_returned_error_factory,
)
from ninja_extended.errors.not_found import NotFoundError, not_found_error_factory
from ninja_extended.errors.not_null_constraint import NotNullConstraintError, not_null_constraint_error_factory
from ninja_extended.errors.protected import ProtectedError, handle_protected_error, protected_error_factory
from ninja_extended.errors.unique_constraint import UniqueConstraintError, unique_constraint_error_factory
from ninja_extended.errors.validation import (
    ValidationError,
    ValidationErrorDetailResponse,
    register_validation_error_handler,
)
