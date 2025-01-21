import pytest
from django.http import HttpRequest

from ninja_extended.api.errors import OperationIdOnRouterAlreadyRegisteredError
from ninja_extended.api.registry import RouterOperationRegistry
from ninja_extended.api.router import ExtendedRouter


@pytest.fixture(name="reset_router_operation_registry", autouse=True)
def reset_router_operation_registry_fixture():
    RouterOperationRegistry.registry = {}


@pytest.fixture(name="router")
def router_fixture():
    return ExtendedRouter(tags=["router"])


def test_extended_router_raises_operation_id_on_router_already_registered(
    router: ExtendedRouter,
):
    router_id = id(router)

    def operation(request: HttpRequest):
        pass

    router.get(
        path="/",
        operation_id="operation_id",
        summary="Summary.",
        description="Description.",
    )(operation)

    with pytest.raises(
        expected_exception=OperationIdOnRouterAlreadyRegisteredError,
        match=f"Operation id 'operation_id' already registered on router with id {router_id}.",
    ):
        router.get(
            path="/",
            operation_id="operation_id",
            summary="Summary.",
            description="Description.",
        )(operation)


def test_extended_router_operation_ids_registered(router: ExtendedRouter):
    def operation(request: HttpRequest):
        pass

    router.get(
        path="/",
        operation_id="operation_id_1",
        summary="Summary.",
        description="Description.",
    )(operation)
    router.get(
        path="/",
        operation_id="operation_id_2",
        summary="Summary.",
        description="Description.",
    )(operation)

    assert RouterOperationRegistry.operation_ids(router=router) == [
        "operation_id_1",
        "operation_id_2",
    ]
