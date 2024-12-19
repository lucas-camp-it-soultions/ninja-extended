from decimal import Decimal

import pytest
from ninja_extended.errors import NotFoundError


class ResourceNotFoundError(NotFoundError):
    resource_name = "Resource"


class FooBarNotFoundError(NotFoundError):
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
    ErrorModel = ResourceNotFoundError.schema()
    path = "/resource/1"
    operation_id = "getResource"

    error = ResourceNotFoundError(fields=fields)
    model = ErrorModel(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/resources/not-found"
    assert model.title == "Resource not found."
    assert (
        model.detail
        == "Resource with (bool_true=true,bool_false=false,deciaml=42.21,float=42.21,int=42,str='foobar') not found."
    )
    assert model.status == 404
    assert model.path == path
    assert model.operation_id == operation_id
    assert model.fields == fields


def test_not_found_error_2(fields):
    ErrorModel = FooBarNotFoundError.schema()
    path = "/foo-bar/1"
    operation_id = "getFooBar"

    error = FooBarNotFoundError(fields=fields)
    model = ErrorModel(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/foo-bars/not-found"
    assert model.title == "FooBar not found."
    assert (
        model.detail
        == "FooBar with (bool_true=true,bool_false=false,deciaml=42.21,float=42.21,int=42,str='foobar') not found."
    )
    assert model.status == 404
    assert model.path == path
    assert model.operation_id == operation_id
    assert model.fields == fields