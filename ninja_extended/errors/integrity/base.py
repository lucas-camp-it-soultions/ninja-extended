"""Module errors.integrity.base."""

from django.db import IntegrityError, connection

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

        if connection.vendor == "sqlite":
            return SQLite3IntegrityErrorParser().parse(error=error)

        raise RuntimeError(parse_error_message_unknown_vendor)
