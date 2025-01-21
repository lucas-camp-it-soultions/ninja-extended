from ninja_extended.errors import AuthorizationError


def test_authentication_error():
    path = "/resource/1"
    operation_id = "getResource"

    error = AuthorizationError(permissions=["app.add_resource", "app.delete_resource"])
    model = AuthorizationError.schema(**error.to_dict(), path=path, operation_id=operation_id)

    assert model.type == "errors/authorization"
    assert model.status == 403
    assert model.permissions == ["app.add_resource", "app.delete_resource"]
    assert model.path == path
    assert model.operation_id == operation_id
