from decimal import Decimal

import pytest

from ninja_extended.errors import NotNullConstraintError


class ResourceNotNullConstraintError(NotNullConstraintError):
    resource_name = "Resource"


class FooBarNotNullConstraintError(NotNullConstraintError):
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
    error_model = ResourceNotNullConstraintError.schema()
    path = "/resource/1"
    operation_id = "getResource"

    error = ResourceNotNullConstraintError(fields=fields)
    model = error_model(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/resources/not-null-constraint"
    assert model.title == "Not null constraint violation for Resource."
    assert (
        model.detail
        == "Not null constraint violation for Resource with (bool_true=true,bool_false=false,deciaml=42.21,float=42.21,int=42,str='foobar')."
    )
    assert model.status == 422
    assert model.path == path
    assert model.operation_id == operation_id
    assert model.fields == fields


def test_not_found_error_2(fields):
    error_model = FooBarNotNullConstraintError.schema()
    path = "/foo-bar/1"
    operation_id = "getFooBar"

    error = FooBarNotNullConstraintError(fields=fields)
    model = error_model(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/foo-bars/not-null-constraint"
    assert model.title == "Not null constraint violation for FooBar."
    assert (
        model.detail
        == "Not null constraint violation for FooBar with (bool_true=true,bool_false=false,deciaml=42.21,float=42.21,int=42,str='foobar')."
    )
    assert model.status == 422
    assert model.path == path
    assert model.operation_id == operation_id
    assert model.fields == fields
