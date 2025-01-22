from typing import Literal, _AnnotatedAlias

import pytest
from django.http import HttpRequest
from ninja import Schema

from ninja_extended.api import ExtendedNinjaAPI, ExtendedRouter, response_factory
from ninja_extended.api.errors import OperationIdNotFoundInAPIError, OperationIdNotFoundInRouterError
from ninja_extended.api.registry import APIOperationRegistry, RouterOperationRegistry
from ninja_extended.api.utils import (
    get_operation_from_api_by_operation_id,
    get_operation_from_router_by_operation_id,
    is_response_registered_in_operation,
)
from ninja_extended.errors import AuthenticationError, AuthorizationError, CSRFError


@pytest.fixture(name="reset_router_operation_registry", autouse=True)
def reset_router_operation_registry_fixture():
    """Fixture for resetting the RouterOperationRegistry."""

    RouterOperationRegistry.registry = {}


@pytest.fixture(name="reset_api_operation_registry", autouse=True)
def reset_api_operation_registry_fixture():
    """Fixture for resetting the APIOperationRegistry."""

    APIOperationRegistry.registry = {}


@pytest.fixture(name="router")
def router_fixture():
    """Fixture for a router instance."""

    return ExtendedRouter(tags=["default"])


@pytest.fixture(name="api")
def api_fixture():
    """Fixture for an API instance."""

    return ExtendedNinjaAPI(title="API", version="1.0.0", description="API description")


@pytest.fixture(name="operation_id")
def operation_id_fixture():
    """Fixture for an operation id."""

    return "operation1"


class SchemaA(Schema):
    type: Literal["a"]
    value_a: str


class SchemaB(Schema):
    type: Literal["b"]
    value_b: str


def test_response_factory_single_schema():
    response_dict = response_factory((200, SchemaA))

    assert isinstance(response_dict, dict)

    assert response_dict == {200: SchemaA}


def test_response_factory_multiple_schemas_different_status():
    response_dict = response_factory((200, SchemaA), (201, SchemaB))

    assert isinstance(response_dict, dict)

    assert response_dict == {200: SchemaA, 201: SchemaB}


def test_response_factory_multiple_schemas_same_status():
    response_dict = response_factory((200, SchemaA), (200, SchemaB))

    assert isinstance(response_dict, dict)
    assert len(response_dict) == 1

    assert isinstance(response_dict[200], _AnnotatedAlias)
    assert len(response_dict[200].__args__) == 1
    assert len(response_dict[200].__args__[0].__args__) == 2
    assert response_dict[200].__args__[0].__args__ == (SchemaA, SchemaB)


def test_response_factory_single_error():
    response_dict = response_factory(AuthenticationError)

    assert isinstance(response_dict, dict)

    assert response_dict == {401: AuthenticationError.schema}


def test_response_factory_multiple_errors_different_status():
    response_dict = response_factory(AuthenticationError, AuthorizationError)

    assert isinstance(response_dict, dict)

    assert response_dict == {401: AuthenticationError.schema, 403: AuthorizationError.schema}


def test_response_factory_multiple_errors_same_status():
    response_dict = response_factory(AuthorizationError, CSRFError)

    assert isinstance(response_dict, dict)
    assert len(response_dict) == 1

    assert isinstance(response_dict[403], _AnnotatedAlias)
    assert len(response_dict[403].__args__) == 1
    assert len(response_dict[403].__args__[0].__args__) == 2
    assert response_dict[403].__args__[0].__args__ == (AuthorizationError.schema, CSRFError.schema)


def test_response_factory_single_schema_multiple_errors():
    response_dict = response_factory((200, SchemaA), AuthenticationError, AuthorizationError, CSRFError)

    assert isinstance(response_dict, dict)
    assert len(response_dict) == 3

    # 200
    assert response_dict[200] == SchemaA

    # 401
    assert response_dict[401] == AuthenticationError.schema

    # 403
    assert isinstance(response_dict[403], _AnnotatedAlias)
    assert len(response_dict[403].__args__) == 1
    assert len(response_dict[403].__args__[0].__args__) == 2
    assert response_dict[403].__args__[0].__args__ == (AuthorizationError.schema, CSRFError.schema)


def test_response_factory_single_list_schema_multiple_errors():
    response_dict = response_factory((200, list[SchemaA]), AuthenticationError, AuthorizationError, CSRFError)

    assert isinstance(response_dict, dict)
    assert len(response_dict) == 3

    # 200
    assert response_dict[200] == list[SchemaA]

    # 401
    assert response_dict[401] == AuthenticationError.schema

    # 403
    assert isinstance(response_dict[403], _AnnotatedAlias)
    assert len(response_dict[403].__args__) == 1
    assert len(response_dict[403].__args__[0].__args__) == 2
    assert response_dict[403].__args__[0].__args__ == (AuthorizationError.schema, CSRFError.schema)


def test_get_operation_from_api_by_operation_id_not_found(api: ExtendedNinjaAPI, operation_id: str):
    api_id = id(api)

    with pytest.raises(
        expected_exception=OperationIdNotFoundInAPIError,
        match=f"Operation id '{operation_id}' not found in api with id {api_id}.",
    ):
        get_operation_from_api_by_operation_id(api=api, operation_id=operation_id)


def test_get_operation_from_router_by_operation_id_not_found(router: ExtendedRouter, operation_id: str):
    router_id = id(router)

    with pytest.raises(
        expected_exception=OperationIdNotFoundInRouterError,
        match=f"Operation id '{operation_id}' not found in router with id {router_id}.",
    ):
        get_operation_from_router_by_operation_id(router=router, operation_id=operation_id)


def test_is_response_registered_in_operation_api_single_schema(
    api: ExtendedNinjaAPI, router: ExtendedRouter, operation_id
):
    def operation(request: HttpRequest):
        pass

    router.get(path="/", operation_id=operation_id, summary="Summary.", response=response_factory((200, SchemaA)))(
        operation
    )
    api.add_router(prefix="", router=router)

    assert is_response_registered_in_operation(api_or_router=api, operation_id=operation_id, response=(200, SchemaA))


def test_is_response_registered_in_operation_api_multiple_schema_different_status(
    api: ExtendedNinjaAPI, router: ExtendedRouter, operation_id
):
    def operation(request: HttpRequest):
        pass

    router.get(
        path="/1",
        operation_id=operation_id,
        summary="Summary.",
        response=response_factory((200, SchemaA), (201, SchemaB)),
    )(operation)
    api.add_router(prefix="", router=router)

    assert is_response_registered_in_operation(api_or_router=api, operation_id=operation_id, response=(200, SchemaA))
    assert is_response_registered_in_operation(api_or_router=api, operation_id=operation_id, response=(201, SchemaB))


def test_is_response_registered_in_operation_api_multiple_schema_same_status(
    api: ExtendedNinjaAPI, router: ExtendedRouter, operation_id
):
    def operation(request: HttpRequest):
        pass

    router.get(
        path="/1",
        operation_id=operation_id,
        summary="Summary.",
        response=response_factory((200, SchemaA), (200, SchemaB)),
    )(operation)
    api.add_router(prefix="", router=router)

    assert is_response_registered_in_operation(api_or_router=api, operation_id=operation_id, response=(200, SchemaA))
    assert is_response_registered_in_operation(api_or_router=api, operation_id=operation_id, response=(200, SchemaB))


def test_is_response_registered_in_operation_api_single_error(
    api: ExtendedNinjaAPI, router: ExtendedRouter, operation_id
):
    def operation(request: HttpRequest):
        pass

    router.get(
        path="/",
        operation_id=operation_id,
        summary="Summary.",
        response=response_factory((200, SchemaA), AuthenticationError),
    )(operation)
    api.add_router(prefix="", router=router)

    assert is_response_registered_in_operation(api_or_router=api, operation_id=operation_id, response=(200, SchemaA))
    assert is_response_registered_in_operation(
        api_or_router=api, operation_id=operation_id, response=AuthenticationError
    )


def test_is_response_registered_in_operation_api_multiple_errors_different_status(
    api: ExtendedNinjaAPI, router: ExtendedRouter, operation_id
):
    def operation(request: HttpRequest):
        pass

    router.get(
        path="/",
        operation_id=operation_id,
        summary="Summary.",
        response=response_factory((200, SchemaA), AuthenticationError, AuthorizationError),
    )(operation)
    api.add_router(prefix="", router=router)

    assert is_response_registered_in_operation(api_or_router=api, operation_id=operation_id, response=(200, SchemaA))
    assert is_response_registered_in_operation(
        api_or_router=api, operation_id=operation_id, response=AuthenticationError
    )
    assert is_response_registered_in_operation(
        api_or_router=api, operation_id=operation_id, response=AuthorizationError
    )


def test_is_response_registered_in_operation_api_multiple_errors_same_status(
    api: ExtendedNinjaAPI, router: ExtendedRouter, operation_id
):
    def operation(request: HttpRequest):
        pass

    router.get(
        path="/",
        operation_id=operation_id,
        summary="Summary.",
        response=response_factory((200, SchemaA), AuthenticationError, CSRFError),
    )(operation)
    api.add_router(prefix="", router=router)

    assert is_response_registered_in_operation(api_or_router=api, operation_id=operation_id, response=(200, SchemaA))
    assert is_response_registered_in_operation(
        api_or_router=api, operation_id=operation_id, response=AuthenticationError
    )
    assert is_response_registered_in_operation(api_or_router=api, operation_id=operation_id, response=CSRFError)


def test_is_response_registered_in_operation_api_multiple_schemas_multiple_errors(
    api: ExtendedNinjaAPI, router: ExtendedRouter, operation_id
):
    def operation(request: HttpRequest):
        pass

    router.get(
        path="/",
        operation_id=operation_id,
        summary="Summary.",
        response=response_factory(
            (200, SchemaA), (201, SchemaA), (201, SchemaB), AuthenticationError, AuthorizationError, CSRFError
        ),
    )(operation)
    api.add_router(prefix="", router=router)

    assert is_response_registered_in_operation(api_or_router=api, operation_id=operation_id, response=(200, SchemaA))
    assert is_response_registered_in_operation(api_or_router=api, operation_id=operation_id, response=(201, SchemaA))
    assert is_response_registered_in_operation(api_or_router=api, operation_id=operation_id, response=(201, SchemaB))
    assert is_response_registered_in_operation(
        api_or_router=api, operation_id=operation_id, response=AuthenticationError
    )
    assert is_response_registered_in_operation(
        api_or_router=api, operation_id=operation_id, response=AuthorizationError
    )
    assert is_response_registered_in_operation(api_or_router=api, operation_id=operation_id, response=CSRFError)


def test_is_response_registered_in_operation_router_single_schema(router: ExtendedRouter, operation_id):
    def operation(request: HttpRequest):
        pass

    router.get(path="/", operation_id=operation_id, summary="Summary.", response=response_factory((200, SchemaA)))(
        operation
    )

    assert is_response_registered_in_operation(api_or_router=router, operation_id=operation_id, response=(200, SchemaA))


def test_is_response_registered_in_operation_router_multiple_schema_different_status(
    router: ExtendedRouter, operation_id
):
    def operation(request: HttpRequest):
        pass

    router.get(
        path="/1",
        operation_id=operation_id,
        summary="Summary.",
        response=response_factory((200, SchemaA), (201, SchemaB)),
    )(operation)

    assert is_response_registered_in_operation(api_or_router=router, operation_id=operation_id, response=(200, SchemaA))
    assert is_response_registered_in_operation(api_or_router=router, operation_id=operation_id, response=(201, SchemaB))


def test_is_response_registered_in_operation_router_multiple_schema_same_status(router: ExtendedRouter, operation_id):
    def operation(request: HttpRequest):
        pass

    router.get(
        path="/1",
        operation_id=operation_id,
        summary="Summary.",
        response=response_factory((200, SchemaA), (200, SchemaB)),
    )(operation)

    assert is_response_registered_in_operation(api_or_router=router, operation_id=operation_id, response=(200, SchemaA))
    assert is_response_registered_in_operation(api_or_router=router, operation_id=operation_id, response=(200, SchemaB))


def test_is_response_registered_in_operation_router_single_error(router: ExtendedRouter, operation_id):
    def operation(request: HttpRequest):
        pass

    router.get(
        path="/",
        operation_id=operation_id,
        summary="Summary.",
        response=response_factory((200, SchemaA), AuthenticationError),
    )(operation)

    assert is_response_registered_in_operation(api_or_router=router, operation_id=operation_id, response=(200, SchemaA))
    assert is_response_registered_in_operation(
        api_or_router=router, operation_id=operation_id, response=AuthenticationError
    )


def test_is_response_registered_in_operation_router_multiple_errors_different_status(
    router: ExtendedRouter, operation_id
):
    def operation(request: HttpRequest):
        pass

    router.get(
        path="/",
        operation_id=operation_id,
        summary="Summary.",
        response=response_factory((200, SchemaA), AuthenticationError, AuthorizationError),
    )(operation)

    assert is_response_registered_in_operation(api_or_router=router, operation_id=operation_id, response=(200, SchemaA))
    assert is_response_registered_in_operation(
        api_or_router=router, operation_id=operation_id, response=AuthenticationError
    )
    assert is_response_registered_in_operation(
        api_or_router=router, operation_id=operation_id, response=AuthorizationError
    )


def test_is_response_registered_in_operation_router_multiple_errors_same_status(router: ExtendedRouter, operation_id):
    def operation(request: HttpRequest):
        pass

    router.get(
        path="/",
        operation_id=operation_id,
        summary="Summary.",
        response=response_factory((200, SchemaA), AuthenticationError, CSRFError),
    )(operation)

    assert is_response_registered_in_operation(api_or_router=router, operation_id=operation_id, response=(200, SchemaA))
    assert is_response_registered_in_operation(
        api_or_router=router, operation_id=operation_id, response=AuthenticationError
    )
    assert is_response_registered_in_operation(api_or_router=router, operation_id=operation_id, response=CSRFError)


def test_is_response_registered_in_operation_router_multiple_schemas_multiple_errors(
    router: ExtendedRouter, operation_id
):
    def operation(request: HttpRequest):
        pass

    router.get(
        path="/",
        operation_id=operation_id,
        summary="Summary.",
        response=response_factory(
            (200, SchemaA), (201, SchemaA), (201, SchemaB), AuthenticationError, AuthorizationError, CSRFError
        ),
    )(operation)

    assert is_response_registered_in_operation(api_or_router=router, operation_id=operation_id, response=(200, SchemaA))
    assert is_response_registered_in_operation(api_or_router=router, operation_id=operation_id, response=(201, SchemaA))
    assert is_response_registered_in_operation(api_or_router=router, operation_id=operation_id, response=(201, SchemaB))
    assert is_response_registered_in_operation(
        api_or_router=router, operation_id=operation_id, response=AuthenticationError
    )
    assert is_response_registered_in_operation(
        api_or_router=router, operation_id=operation_id, response=AuthorizationError
    )
    assert is_response_registered_in_operation(api_or_router=router, operation_id=operation_id, response=CSRFError)
