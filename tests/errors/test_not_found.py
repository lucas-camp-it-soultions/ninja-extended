from decimal import Decimal

import pytest

from ninja_extended.errors import NotFoundError, not_found_error_factory


class ResourceNotFoundError(NotFoundError):
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
        ResourceNotFoundError,
        not_found_error_factory(resource_="Resource"),
    ],
)
def test_not_found_error(error_class: type[NotFoundError], fields):
    path = "/resource/1"
    operation_id = "getResource"

    error = error_class(fields=fields)
    model = error_class.schema(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/not-found"
    assert model.status == 404
    assert model.resource == "Resource"
    assert model.fields == fields
    assert model.path == path
    assert model.operation_id == operation_id
