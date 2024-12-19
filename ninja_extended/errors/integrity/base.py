"""Module errors.integrity.base."""

from sqlite3 import IntegrityError as SQLite3IntegrityError

from django.db import IntegrityError
from psycopg2.errors import NotNullViolation, UniqueViolation

from ninja_extended.errors.integrity.postgres import PostgresIntegrityErrorParser
from ninja_extended.errors.integrity.sqlite3 import SQLite3IntegrityErrorParser


class IntegrityErrorParser:
    """Parser for integrity error for SQLite3."""

    def parse(self, error: IntegrityError) -> list[str]:
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
