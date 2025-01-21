import pytest

from ninja_extended.errors import ProtectedError


class ResourceProtectedError(ProtectedError):
    resource = "Resource"


@pytest.fixture
def foreign_items():
    return {
        "Child1": [1],
        "Child2": [2, 3],
    }


def test_protected_error(foreign_items):
    path = "/resource/1"
    operation_id = "getResource"

    error = ResourceProtectedError(foreign_items=foreign_items)
    model = ResourceProtectedError.schema(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/protection"
    assert model.status == 422
    assert model.resource == "Resource"
    assert model.foreign_items == foreign_items
    assert model.path == path
    assert model.operation_id == operation_id
