from ninja_extended.errors import AuthenticationError


def test_authentication_error():
    path = "/resource/1"
    operation_id = "getResource"

    error = AuthenticationError()
    model = AuthenticationError.schema(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/authentication"
    assert model.status == 401
    assert model.path == path
    assert model.operation_id == operation_id
