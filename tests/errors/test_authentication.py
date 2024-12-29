from ninja_extended.errors import AuthenticationError


def test_authentication_error():
    error_model = AuthenticationError.schema()
    path = "/resource/1"
    operation_id = "getResource"

    error = AuthenticationError()
    model = error_model(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/auth/authentication"
    assert model.title == "Not authenticated."
    assert model.detail == "Not authenticated."
    assert model.status == 401
    assert model.path == path
    assert model.operation_id == operation_id
