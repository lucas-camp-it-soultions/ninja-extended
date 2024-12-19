"""Module error.integrity."""

# ruff: noqa: F401

from ninja_extended.errors.integrity.base import IntegrityErrorParser
from ninja_extended.errors.integrity.sqlite3 import (
    SQLite3IntegrityErrorParser,
    SQLite3NotNullIntegrityErrorParser,
    SQLite3UniqueConstraintIntegrityErrorParser,
)
