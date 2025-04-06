import pytest

from ninja_extended.errors import CheckConstraintError, check_constraint_error_factory

from .resource_errors import ResourceErrors


class ResourceCheckConstraintError(CheckConstraintError):
    resource = "Resource"


@pytest.mark.parametrize(
    "error_class",
    [
        ResourceCheckConstraintError,
        check_constraint_error_factory(resource_="Resource"),
        ResourceErrors.CheckConstraint,
    ],
)
def test_check_error(error_class: type[CheckConstraintError]):
    path = "/resource/1"
    operation_id = "getResource"

    error = error_class()
    model = error_class.schema(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/check-constraint"
    assert model.status == 422
    assert model.path == path
    assert model.operation_id == operation_id
