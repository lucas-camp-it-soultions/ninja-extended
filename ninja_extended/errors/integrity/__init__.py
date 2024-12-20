"""Module error.integrity."""

# ruff: noqa: F401

from ninja_extended.errors.integrity.base import IntegrityErrorParser, handle_integrity_error
from ninja_extended.errors.integrity.postgres import (
    PostgresIntegrityErrorParser,
    PostgresNotNullIntegrityErrorParser,
    PostgresUniqueConstraintIntegrityErrorParser,
)
from ninja_extended.errors.integrity.sqlite3 import (
    SQLite3IntegrityErrorParser,
    SQLite3NotNullIntegrityErrorParser,
    SQLite3UniqueConstraintIntegrityErrorParser,
)
