from decimal import Decimal

import pytest

from ninja_extended.errors import MultipleObjectsReturnedError


class ResourceMultipleObjectsReturnedError(MultipleObjectsReturnedError):
    resource_name = "Resource"


class FooBarMultipleObjectsReturnedError(MultipleObjectsReturnedError):
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


def test_multiple_objects_returned_error(fields):
    error_model = ResourceMultipleObjectsReturnedError.schema()
    path = "/resource/1"
    operation_id = "getResource"

    error = ResourceMultipleObjectsReturnedError(fields=fields)
    model = error_model(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/resources/multiple-objects-returned"
    assert model.title == "Multiple Resource objects returned."
    assert (
        model.detail
        == "Multiple Resource objects with (bool_true=true,bool_false=false,deciaml=42.21,float=42.21,int=42,str='foobar') returned."
    )
    assert model.status == 422
    assert model.path == path
    assert model.operation_id == operation_id
    assert model.fields == fields


def test_multiple_objects_returned_error_2(fields):
    error_model = FooBarMultipleObjectsReturnedError.schema()
    path = "/foo-bar/1"
    operation_id = "getFooBar"

    error = FooBarMultipleObjectsReturnedError(fields=fields)
    model = error_model(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/foo-bars/multiple-objects-returned"
    assert model.title == "Multiple FooBar objects returned."
    assert (
        model.detail
        == "Multiple FooBar objects with (bool_true=true,bool_false=false,deciaml=42.21,float=42.21,int=42,str='foobar') returned."
    )
    assert model.status == 422
    assert model.path == path
    assert model.operation_id == operation_id
    assert model.fields == fields
