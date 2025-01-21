from ninja_extended.errors import CSRFError


def test_authentication_error():
    path = "/resource/1"
    operation_id = "getResource"

    error = CSRFError()
    model = CSRFError.schema(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/csrf"
    assert model.status == 403
    assert model.path == path
    assert model.operation_id == operation_id
