from ninja_extended.errors import AuthorizationError


def test_authentication_error():
    error_model = AuthorizationError.schema()
    path = "/resource/1"
    operation_id = "getResource"

    error = AuthorizationError(operation="operation")
    model = error_model(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/auth/authorization"
    assert model.title == "Unsufficient permissions for the operation."
    assert model.detail == "Unsufficient permissions for the operation 'operation'."
    assert model.status == 403
    assert model.operation == "operation"
    assert model.path == path
    assert model.operation_id == operation_id
