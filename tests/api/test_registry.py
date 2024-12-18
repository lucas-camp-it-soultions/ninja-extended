"""Tests for APIOperationRegistry and RouterOperationRegistry."""

import pytest
from ninja import NinjaAPI, Router

from ninja_extended.api.errors import (
    APIAlreadyRegisteredError,
    APINotRegisteredError,
    OperationIdOnAPIAlreadyRegisteredError,
    OperationIdOnRouterAlreadyRegisteredError,
    RouterAlreadyRegisteredError,
    RouterNotRegisteredError,
)
from ninja_extended.api.registry import APIOperationRegistry, RouterOperationRegistry


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

    return Router()


@pytest.fixture(name="router_2")
def router2_fixture():
    """Fixture for another router instance."""

    return Router()


@pytest.fixture(name="api")
def api_fixture():
    """Fixture for an API instance."""

    return NinjaAPI()


@pytest.fixture(name="operation_id")
def operation_id_fixture():
    """Fixture for an operation id."""

    return "operation1"


@pytest.fixture(name="operation_id_2")
def operation_id_2_fixture():
    """Fixture for another operation id."""

    return "operation2"


def test_router_registry_is_empty():
    """Test that the initial RouterOperationRegistry is empty."""

    assert RouterOperationRegistry.registry == {}


def test_router_registry_register_router_raises_router_already_registered(router: Router):
    """Test that an Error is raised, if a router is registered more than once."""

    RouterOperationRegistry.register_router(router=router)
    router_id = id(router)

    with pytest.raises(
        expected_exception=RouterAlreadyRegisteredError,
        match=f"Router with id {router_id} already registered.",
    ):
        RouterOperationRegistry.register_router(router=router)


def test_router_registry_register_router(router: Router):
    """Test that a router is registered successfully and has no operation ids."""

    RouterOperationRegistry.register_router(router=router)
    router_id = id(router)

    assert RouterOperationRegistry.registry == {router_id: []}


def test_router_registry_register_operation_id_raises_router_not_registered(router: Router, operation_id: str):
    """Test that an Error is raised, if an operation id is registered but the router is not registered."""

    router_id = id(router)

    with pytest.raises(
        expected_exception=RouterNotRegisteredError,
        match=f"Router with id {router_id} is not registered.",
    ):
        RouterOperationRegistry.register_operation_id(router=router, operation_id=operation_id)


def test_router_registry_register_operation_id_raises_operation_id_on_router_already_registered(
    router: Router, operation_id: str
):
    """Test that an Error is raised, if an operation id is registered that is already registered."""

    RouterOperationRegistry.register_router(router=router)
    RouterOperationRegistry.register_operation_id(router=router, operation_id=operation_id)
    router_id = id(router)

    with pytest.raises(
        expected_exception=OperationIdOnRouterAlreadyRegisteredError,
        match=f"Operation id '{operation_id}' already registered on router with id {router_id}.",
    ):
        RouterOperationRegistry.register_operation_id(router=router, operation_id=operation_id)


def test_router_registry_register_operation_id(router: Router, operation_id: str):
    """Test that a registered operation ids are written into the registry."""

    RouterOperationRegistry.register_router(router=router)
    RouterOperationRegistry.register_operation_id(router=router, operation_id=operation_id)
    router_id = id(router)

    assert RouterOperationRegistry.registry == {router_id: ["operation1"]}


def test_router_registry_operation_ids(router: Router, operation_id: str):
    """Test that the correct registered operation ids are returned."""

    RouterOperationRegistry.register_router(router=router)
    RouterOperationRegistry.register_operation_id(router=router, operation_id=operation_id)

    assert RouterOperationRegistry.operation_ids(router=router) == ["operation1"]


def test_api_registry_is_empty():
    """Test that the initial APIOperationRegistry is empty."""

    assert APIOperationRegistry.registry == {}


def test_api_registry_register_router_raises_api_already_registered(api: NinjaAPI):
    """Test that an Error is raised, if an API is registered more than once."""

    APIOperationRegistry.register_api(api=api)
    api_id = id(api)

    with pytest.raises(
        expected_exception=APIAlreadyRegisteredError,
        match=f"API with id {api_id} already registered.",
    ):
        APIOperationRegistry.register_api(api=api)


def test_api_registry_register_api(api: Router):
    """Test that an API is registered successfully and has no operation ids."""

    APIOperationRegistry.register_api(api=api)
    api_id = id(api)

    assert APIOperationRegistry.registry == {api_id: []}


def test_api_registry_register_routers_operation_ids_raises_api_not_registered(api: NinjaAPI, router: Router):
    """Test that an Error is raised, if an operation id is registered but the API is not registered."""
    api_id = id(api)

    with pytest.raises(
        expected_exception=APINotRegisteredError,
        match=f"API with id {api_id} is not registered.",
    ):
        APIOperationRegistry.register_routers_operation_ids(api=api, router=router)


def test_api_registry_register_routers_operation_ids_raises_operation_id_on_api_already_registered(
    api: NinjaAPI, router: Router, router_2: Router, operation_id: str
):
    """Test that an Error is raised, if an operation id from a router is registered that is already registered from another router."""

    APIOperationRegistry.register_api(api=api)
    RouterOperationRegistry.register_router(router=router)
    RouterOperationRegistry.register_operation_id(router=router, operation_id=operation_id)
    RouterOperationRegistry.register_router(router=router_2)
    RouterOperationRegistry.register_operation_id(router=router_2, operation_id=operation_id)
    APIOperationRegistry.register_routers_operation_ids(api=api, router=router)
    api_id = id(api)

    with pytest.raises(
        expected_exception=OperationIdOnAPIAlreadyRegisteredError,
        match=f"Operation id '{operation_id}' already registered on api with id {api_id}.",
    ):
        APIOperationRegistry.register_routers_operation_ids(api=api, router=router_2)


def test_api_registry_register_routers_operation_ids(
    api: NinjaAPI,
    router: Router,
    router_2: Router,
    operation_id: str,
    operation_id_2: str,
):
    """Test that a registered operation ids are written into the registry."""

    APIOperationRegistry.register_api(api=api)
    RouterOperationRegistry.register_router(router=router)
    RouterOperationRegistry.register_operation_id(router=router, operation_id=operation_id)
    APIOperationRegistry.register_routers_operation_ids(api=api, router=router)
    RouterOperationRegistry.register_router(router=router_2)
    RouterOperationRegistry.register_operation_id(router=router_2, operation_id=operation_id_2)
    APIOperationRegistry.register_routers_operation_ids(api=api, router=router_2)
    api_id = id(api)

    assert APIOperationRegistry.registry == {api_id: ["operation1", "operation2"]}


def test_api_registry_operation_ids(
    api: NinjaAPI,
    router: Router,
    router_2: Router,
    operation_id: str,
    operation_id_2: str,
):
    """Test that the correct registered operation ids are returned."""

    APIOperationRegistry.register_api(api=api)
    RouterOperationRegistry.register_router(router=router)
    RouterOperationRegistry.register_operation_id(router=router, operation_id=operation_id)
    APIOperationRegistry.register_routers_operation_ids(api=api, router=router)
    RouterOperationRegistry.register_router(router=router_2)
    RouterOperationRegistry.register_operation_id(router=router_2, operation_id=operation_id_2)
    APIOperationRegistry.register_routers_operation_ids(api=api, router=router_2)

    assert APIOperationRegistry.operation_ids(api=api) == ["operation1", "operation2"]
