import pytest

from ninja_extended.errors import ProtectedError, protected_error_factory


class ResourceProtectedError(ProtectedError):
    resource = "Resource"


@pytest.fixture
def foreign_items():
    return {
        "Child1": [1],
        "Child2": [2, 3],
    }


@pytest.mark.parametrize(
    "error_class",
    [
        ResourceProtectedError,
        protected_error_factory(resource_="Resource"),
    ],
)
def test_protected_error(error_class: type[ProtectedError], foreign_items):
    path = "/resource/1"
    operation_id = "getResource"

    error = error_class(foreign_items=foreign_items)
    model = error_class.schema(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/protection"
    assert model.status == 422
    assert model.resource == "Resource"
    assert model.foreign_items == foreign_items
    assert model.path == path
    assert model.operation_id == operation_id
