"""Module error.integrity."""

import re
from re import Pattern

from django.db import IntegrityError

from ninja_extended.errors.integrity.types import IntegrityErrorType


class PostgresUniqueConstraintIntegrityErrorParser:
    """Parser for unique constraint error for Postgres."""

    pattern: Pattern[str] = (
        r"duplicate key value violates unique constraint \"(?P<constraint_name>.*)\"\nDETAIL:\s*Key \((?P<columns_string>.*)\)=\((?P<values_string>.*)\) already exists.\n"
    )

    def parse(self, error: IntegrityError) -> tuple[IntegrityErrorType, list[str]]:
        """Parse IntegrityError.

        Args:
            error (IntegrityError): The integrity error.

        Raises:
            RuntimeError: If the error can not be parsed.

        Returns:
           tuple[IntegrityErrorType, list[str]]: The column names violating the unique constraint.
        """

        parse_error_message_multiple_args = (
            "Unable to parse Integrity Error. IntegrityError was instantiated with multiple args."
        )
        parse_error_message_multiple_pattern_not_found = "Unable to parse Integrity Error. Pattern not Found."
        parse_error_message_multiple_no_columns_detected = "Unable to parse Integrity Error. No columns detected."

        if len(error.args) != 1:
            raise RuntimeError(parse_error_message_multiple_args)

        arg = error.args[0]

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

        return IntegrityErrorType.UNIQUE_CONSTRAINT, columns


class PostgresNotNullIntegrityErrorParser:
    """Parser for not null error for Postgres."""

    pattern: Pattern[str] = (
        r"null value in column \"(?P<column_string>.*)\" of relation \"(?P<relation_name>.*)\" violates not-null constraint\nDETAIL:\s*Failing row contains \((?P<values_string>.*)\).\n"
    )

    def parse(self, error: IntegrityError) -> tuple[IntegrityErrorType, list[str]]:
        """Parse IntegrityError.

        Args:
            error (IntegrityError): The integrity error.

        Raises:
            RuntimeError: If the error can not be parsed.

        Returns:
           tuple[IntegrityErrorType, list[str]]: The column name violating the not null constraint.
        """

        parse_error_message_multiple_args = (
            "Unable to parse Integrity Error. IntegrityError was instantiated with multiple args."
        )
        parse_error_message_pattern_not_found = "Unable to parse Integrity Error. Pattern not Found."
        parse_error_message_no_columns_detected = "Unable to parse Integrity Error. No columns detected."

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

        return IntegrityErrorType.NOT_NULL_CONSTRAINT, [column_string]


class PostgresCheckIntegrityErrorParser:
    """Parser for check error for Postgres."""

    pattern: Pattern[str] = (
        r"new row for relation \"(?P<relation_name>.*)\" violates check constraint \"(?P<constraint_name>.*)\"\nDETAIL:\s*Failing row contains \((?P<values_string>.*)\).\n"
    )

    def parse(self, error: IntegrityError) -> tuple[IntegrityErrorType, list[str]]:
        """Parse IntegrityError.

        Args:
            error (IntegrityError): The integrity error.

        Raises:
            RuntimeError: If the error can not be parsed.

        Returns:
           tuple[IntegrityErrorType, list[str]]: The column name violating the check constraint.
        """

        parse_error_message_multiple_args = (
            "Unable to parse Integrity Error. IntegrityError was instantiated with multiple args."
        )
        parse_error_message_pattern_not_found = "Unable to parse Integrity Error. Pattern not Found."
        parse_error_message_no_columns_detected = "Unable to parse Integrity Error. No columns detected."

        if len(error.args) != 1:
            raise RuntimeError(parse_error_message_multiple_args)

        arg = error.args[0]

        match = re.match(pattern=self.pattern, string=arg)

        if match is None:
            raise RuntimeError(parse_error_message_pattern_not_found)

        try:
            constraint_name = match.group("constraint_name")
        except IndexError:
            raise RuntimeError(parse_error_message_no_columns_detected)  # noqa: B904

        return IntegrityErrorType.CHECK_CONSTRAINT, [constraint_name]


class PostgresIntegrityErrorParser:
    """Parser for integrity error for Postgres."""

    def parse(self, error: IntegrityError) -> tuple[IntegrityErrorType, list[str]]:
        """Parse IntegrityError.

        Args:
            error (IntegrityError): The integrity error.

        Raises:
            RuntimeError: If the error can not be parsed.

        Returns:
           tuple[IntegrityErrorType, list[str]]: The column name violating the constraint.
        """

        parse_error_message_multiple_args = (
            "Unable to parse Integrity Error. IntegrityError was instantiated with multiple args."
        )
        parse_error_message_unknown_error_type = "Unable to parse Integrity Error. Unknown error type."

        if len(error.args) != 1:
            raise RuntimeError(parse_error_message_multiple_args)

        arg = error.args[0]

        if arg.startswith("null value in column"):
            return PostgresNotNullIntegrityErrorParser().parse(error=error)

        if arg.startswith("duplicate key value violates unique constraint"):
            return PostgresUniqueConstraintIntegrityErrorParser().parse(error=error)

        if "violates check constraint" in arg:
            return PostgresCheckIntegrityErrorParser().parse(error=error)

        raise RuntimeError(parse_error_message_unknown_error_type)
