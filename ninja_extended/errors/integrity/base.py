"""Module errors.integrity.base."""

from sqlite3 import IntegrityError as SQLite3IntegrityError
from typing import Any

from django.db import IntegrityError
from psycopg2.errors import NotNullViolation, UniqueViolation

from ninja_extended.errors.integrity.postgres import PostgresIntegrityErrorParser
from ninja_extended.errors.integrity.sqlite3 import SQLite3IntegrityErrorParser
from ninja_extended.errors.integrity.types import IntegrityErrorType
from ninja_extended.errors.not_null_constraint import NotNullConstraintError
from ninja_extended.errors.unique_constraint import UniqueConstraintError


class IntegrityErrorParser:
    """Parser for integrity error for SQLite3."""

    def parse(self, error: IntegrityError) -> tuple[IntegrityErrorType, list[str]]:
        """Parse IntegrityError.

        Args:
            error (IntegrityError): The integrity error.

        Raises:
            RuntimeError: If the error can not be parsed.

        Returns:
            list[str]: The column name violating the constraint.
        """

        parse_error_message_unknown_vendor = "Unable to parse Integrity Error. Unknown database vendor."

        if isinstance(error.__cause__, NotNullViolation | UniqueViolation):
            return PostgresIntegrityErrorParser().parse(error=error)

        if isinstance(error.__cause__, SQLite3IntegrityError):
            return SQLite3IntegrityErrorParser().parse(error=error)

        raise RuntimeError(parse_error_message_unknown_vendor)


def handle_integrity_error(
    error: IntegrityError,
    unique_constraint_error_type: type[UniqueConstraintError],
    not_null_constraint_error_type: type[NotNullConstraintError],
    data: Any = None,
):
    """Handle IntegrityError.

    Args:
        error (IntegrityError): The error.
        unique_constraint_error_type (type[UniqueConstraintError]): The unique constraint error type.
        not_null_constraint_error_type (type[NotNullConstraintError]): The not null constraint error type.
        data (Any): The data.

    Raises:
        unique_constraint_error_type: If a unique constraint error have been parsed.
        not_null_constraint_error_type: If a not null constraint error have been parsed.
    """

    integrity_error_type, columns = IntegrityErrorParser().parse(error=error)

    if integrity_error_type == IntegrityErrorType.UNIQUE_CONSTRAINT:
        raise unique_constraint_error_type({key: data.model_dump()[key] for key in columns})

    if integrity_error_type == IntegrityErrorType.NOT_NULL_CONSTRAINT:
        raise not_null_constraint_error_type({key: data.model_dump()[key] for key in columns})
