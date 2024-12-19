"""Module error.integrity."""

import re
from re import Pattern

from django.db import IntegrityError


class SQLite3UniqueConstraintIntegrityErrorParser:
    """Parser for unique constraint error for SQLite3."""

    pattern: Pattern[str] = r"UNIQUE constraint failed: (?P<columns_string>.*)"

    def parse(self, error: IntegrityError) -> list[str]:
        """Parse IntegrityError.

        Args:
            error (IntegrityError): The integrity error.

        Raises:
            RuntimeError: If the error can not be parsed.

        Returns:
            list[str]: The column names violating the unique constraint.
        """

        parse_error_message_multiple_args = (
            "Unable to parse Integrity Error. IntegrityError was instantiated with multiple args."
        )
        parse_error_message_multiple_pattern_not_found = "Unable to parse Integrity Error. Pattern not Found."
        parse_error_message_multiple_no_columns_detected = "Unable to parse Integrity Error. No columns detected."
        parse_error_message_multiple_column_not_parsable = "Unable to parse Integrity Error. Column not parsable."

        if len(error.args) != 1:
            raise RuntimeError(parse_error_message_multiple_args)

        arg = error.args[0]
        column_names: list[str] = []

        match = re.match(pattern=self.pattern, string=arg)

        if match is None:
            raise RuntimeError(parse_error_message_multiple_pattern_not_found)

        try:
            columns_string = match.group("columns_string")
        except IndexError:
            raise RuntimeError(parse_error_message_multiple_no_columns_detected)  # noqa: B904

        columns = columns_string.split(", ")

        if len(columns) == 0:
            raise RuntimeError(parse_error_message_multiple_no_columns_detected)

        for column in columns:
            split_column = column.split(".")

            if len(split_column) != 2:  # noqa: PLR2004
                raise RuntimeError(parse_error_message_multiple_column_not_parsable)

            column_names.append(split_column[1])

        return column_names


class SQLite3NotNullIntegrityErrorParser:
    """Parser for not null error for SQLite3."""

    pattern: Pattern[str] = r"NOT NULL constraint failed: (?P<column_string>.*)"

    def parse(self, error: IntegrityError) -> list[str]:
        """Parse IntegrityError.

        Args:
            error (IntegrityError): The integrity error.

        Raises:
            RuntimeError: If the error can not be parsed.

        Returns:
            list[str]: The column name violating the not null constraint.
        """

        parse_error_message_multiple_args = (
            "Unable to parse Integrity Error. IntegrityError was instantiated with multiple args."
        )
        parse_error_message_pattern_not_found = "Unable to parse Integrity Error. Pattern not Found."
        parse_error_message_no_columns_detected = "Unable to parse Integrity Error. No columns detected."
        parse_error_message_column_not_parsable = "Unable to parse Integrity Error. Column not parsable."

        if len(error.args) != 1:
            raise RuntimeError(parse_error_message_multiple_args)

        arg = error.args[0]

        match = re.match(pattern=self.pattern, string=arg)

        if match is None:
            raise RuntimeError(parse_error_message_pattern_not_found)

        try:
            column_string = match.group("column_string")
        except IndexError:
            raise RuntimeError(parse_error_message_no_columns_detected)  # noqa: B904

        split_column = column_string.split(".")

        if len(split_column) != 2:  # noqa: PLR2004
            raise RuntimeError(parse_error_message_column_not_parsable)

        return [split_column[1]]


class SQLite3IntegrityErrorParser:
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

        parse_error_message_multiple_args = (
            "Unable to parse Integrity Error. IntegrityError was instantiated with multiple args."
        )
        parse_error_message_multiple_unknown_error_type = "Unable to parse Integrity Error. Unknown error type."

        if len(error.args) != 1:
            raise RuntimeError(parse_error_message_multiple_args)

        arg = error.args[0]

        if arg.startswith("NOT NULL constraint failed"):
            return SQLite3NotNullIntegrityErrorParser().parse(error=error)

        if arg.startswith("UNIQUE constraint failed"):
            return SQLite3UniqueConstraintIntegrityErrorParser().parse(error=error)

        raise RuntimeError(parse_error_message_multiple_unknown_error_type)
