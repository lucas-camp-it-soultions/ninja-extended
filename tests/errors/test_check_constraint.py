from ninja_extended.errors import CheckConstraintError


class ResourceCheckConstraintError(CheckConstraintError):
    resource = "Resource"


def test_check_error():
    path = "/resource/1"
    operation_id = "getResource"

    error = ResourceCheckConstraintError()
    model = ResourceCheckConstraintError.schema(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/check-constraint"
    assert model.status == 422
    assert model.path == path
    assert model.operation_id == operation_id
