"""Module errors."""

# ruff: noqa: F401

from ninja_extended.errors.base import APIError, APIErrorResponse, register_exception_handler
from ninja_extended.errors.not_found import NotFoundError
from ninja_extended.errors.not_null_constraint import NotNullConstraintError
from ninja_extended.errors.unique_constraint import UniqueConstraintError
from ninja_extended.errors.validation import ValidationError, ValidationErrorDetail
