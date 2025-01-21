from decimal import Decimal

import pytest

from ninja_extended.errors import UniqueConstraintError


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


def test_unique_constraint_error(fields):
    path = "/resource/1"
    operation_id = "getResource"

    error = ResourceUniqueConstraintError(fields=fields)
    model = ResourceUniqueConstraintError.schema(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/unique-constraint"
    assert model.status == 422
    assert model.resource == "Resource"
    assert model.fields == fields
    assert model.path == path
    assert model.operation_id == operation_id
