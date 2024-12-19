from decimal import Decimal

import pytest
from ninja_extended.errors import UniqueConstraintError


class ResourceUniqueConstraintError(UniqueConstraintError):
    resource_name = "Resource"


class FooBarUniqueConstraintError(UniqueConstraintError):
    resource_name = "FooBar"


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


def test_not_found_error(fields):
    ErrorModel = ResourceUniqueConstraintError.schema()
    path = "/resource/1"
    operation_id = "getResource"

    error = ResourceUniqueConstraintError(fields=fields)
    model = ErrorModel(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/resources/unique-constraint"
    assert model.title == "Unique constraint violation for Resource."
    assert (
        model.detail
        == "Unique constraint violation for Resource with (bool_true=true,bool_false=false,deciaml=42.21,float=42.21,int=42,str='foobar')."
    )
    assert model.status == 422
    assert model.path == path
    assert model.operation_id == operation_id
    assert model.fields == fields


def test_not_found_error_2(fields):
    ErrorModel = FooBarUniqueConstraintError.schema()
    path = "/foo-bar/1"
    operation_id = "getFooBar"

    error = FooBarUniqueConstraintError(fields=fields)
    model = ErrorModel(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/foo-bars/unique-constraint"
    assert model.title == "Unique constraint violation for FooBar."
    assert (
        model.detail
        == "Unique constraint violation for FooBar with (bool_true=true,bool_false=false,deciaml=42.21,float=42.21,int=42,str='foobar')."
    )
    assert model.status == 422
    assert model.path == path
    assert model.operation_id == operation_id
    assert model.fields == fields