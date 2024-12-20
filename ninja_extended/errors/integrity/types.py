"""Module errors.integrity.types."""

from enum import Enum


class IntegrityErrorType(str, Enum):
    """Enum for integrity error types."""

    NOT_NULL_CONSTRAINT = "NOT_NULL_CONSTRAINT"
    UNIQUE_CONSTRAINT = "UNIQUE_CONSTRAINT"
