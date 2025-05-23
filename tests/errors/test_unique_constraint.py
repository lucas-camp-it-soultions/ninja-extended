from decimal import Decimal

import pytest

from ninja_extended.errors import UniqueConstraintError, unique_constraint_error_factory

from .resource_errors import ResourceErrors


class ResourceUniqueConstraintError(UniqueConstraintError):
    resource = "Resource"


@pytest.fixture
def fields():
    return {
        "bool_true": True,
        "bool_false": False,
        "deciaml": Decimal("42.21"),
        "float": 42.21,
        "int": 42,
        "str": "foobar",
    }


@pytest.mark.parametrize(
    "error_class",
    [
        ResourceUniqueConstraintError,
        unique_constraint_error_factory(resource_="Resource"),
        ResourceErrors.UniqueConstraint,
    ],
)
def test_unique_constraint_error(error_class: type[UniqueConstraintError], fields):
    path = "/resource/1"
    operation_id = "getResource"

    error = error_class(fields=fields)
    model = error_class.schema(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/unique-constraint"
    assert model.status == 422
    assert model.resource == "Resource"
    assert model.fields == fields
    assert model.path == path
    assert model.operation_id == operation_id
