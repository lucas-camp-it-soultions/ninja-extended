from ninja_extended.errors import CSRFError


def test_authentication_error():
    error_model = CSRFError.schema()
    path = "/resource/1"
    operation_id = "getResource"

    error = CSRFError()
    model = error_model(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/auth/csrf"
    assert model.title == "CSRF check failed."
    assert model.detail == "CSRF check failed."
    assert model.status == 403
    assert model.path == path
    assert model.operation_id == operation_id
