import pytest
from django.http import HttpRequest

from ninja_extended.api.api import ExtendedNinjaAPI
from ninja_extended.api.errors import OperationIdOnAPIAlreadyRegisteredError
from ninja_extended.api.registry import APIOperationRegistry
from ninja_extended.api.router import ExtendedRouter


@pytest.fixture(name="api")
def api_fixture():
    return ExtendedNinjaAPI(title="API", version="1.0.0", description="Description")


@pytest.fixture(name="router_1")
def router_1_fixture():
    return ExtendedRouter()


@pytest.fixture(name="router_2")
def router_2_fixture():
    return ExtendedRouter()


def test_extended_api_raises_operation_id_on_api_already_registered(
    api: ExtendedNinjaAPI, router_1: ExtendedRouter, router_2: ExtendedRouter
):
    api_id = id(api)

    def operation(request: HttpRequest):
        pass

    router_1.get(
        path="/",
        operation_id="operation_id",
        summary="Summary.",
        description="Description.",
        tags=["tag"],
    )(operation)
    router_2.get(
        path="/",
        operation_id="operation_id",
        summary="Summary.",
        description="Description.",
        tags=["tag"],
    )(operation)

    api.add_router(prefix="/1", router=router_1)
    
    with pytest.raises(
        expected_exception=OperationIdOnAPIAlreadyRegisteredError,
        match=f"Operation id 'operation_id' already registered on api with id {api_id}.",
    ):
        api.add_router(prefix="/2", router=router_2)


def test_extended_router_operation_ids_registered(
    api: ExtendedNinjaAPI, router_1: ExtendedRouter, router_2: ExtendedRouter
):
    def operation(request: HttpRequest):
        pass

    router_1.get(
        path="/",
        operation_id="operation_id_1",
        summary="Summary.",
        description="Description.",
        tags=["tag"],
    )(operation)
    router_2.get(
        path="/",
        operation_id="operation_id_2",
        summary="Summary.",
        description="Description.",
        tags=["tag"],
    )(operation)

    api.add_router(prefix="/1", router=router_1)
    api.add_router(prefix="/2", router=router_2)

    assert APIOperationRegistry.operation_ids(api=api) == [
        "operation_id_1",
        "operation_id_2",
    ]
