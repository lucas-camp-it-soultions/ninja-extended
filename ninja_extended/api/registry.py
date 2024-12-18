"""Operation id registries for router and API."""

from typing import ClassVar

from ninja import NinjaAPI, Router

from ninja_extended.api.errors import (
    APIAlreadyRegisteredError,
    APINotRegisteredError,
    OperationIdOnAPIAlreadyRegisteredError,
    OperationIdOnRouterAlreadyRegisteredError,
    RouterAlreadyRegisteredError,
    RouterNotRegisteredError,
)


class RouterOperationRegistry:
    """Operation id registry for router."""

    registry: ClassVar[dict[int, list[str]]] = {}

    @classmethod
    def register_router(cls, router: Router):
        """Register a router in the registry.

        Args:
            router (Router): The router.

        Raises:
            RouterAlreadyRegisteredError: If the router is already registered.
        """
        router_id = id(router)

        if router_id in cls.registry:
            raise RouterAlreadyRegisteredError(router=router)

        cls.registry[router_id] = []

    @classmethod
    def register_operation_id(cls, router: Router, operation_id: str):
        """Register an operation id for a router.

        Args:
            router (Router): The router.
            operation_id (str): The operation id.

        Raises:
            RouterNotRegisteredError: If  the router is not registered.
            OperationIdOnRouterAlreadyRegisteredError: If the oepration id as already registered for the router.
        """
        router_id = id(router)

        if router_id not in cls.registry:
            raise RouterNotRegisteredError(router=router)

        if operation_id in cls.registry[router_id]:
            raise OperationIdOnRouterAlreadyRegisteredError(router=router, operation_id=operation_id)

        cls.registry[router_id].append(operation_id)

    @classmethod
    def operation_ids(cls, router: Router) -> list[str]:
        """Get all registered oepration ids registered for a router.

        Args:
            router (Router): The router.

        Raises:
            RouterNotRegisteredError: If the router is not registered.

        Returns:
            list[str]: The operation ids registered for the router.
        """
        router_id = id(router)

        if router_id not in cls.registry:
            raise RouterNotRegisteredError(router=router)

        return cls.registry[router_id]


class APIOperationRegistry:
    """Operation id registry for API."""

    registry: ClassVar[dict[int, list[str]]] = {}

    @classmethod
    def register_api(cls, api: NinjaAPI):
        """Register an API in the registry.

        Args:
            api (NinjaAPI): The API.

        Raises:
            RouterAlreadyRegisteredError: If the router is already registered.
        """
        api_id = id(api)

        if api_id in cls.registry:
            raise APIAlreadyRegisteredError(api=api)

        cls.registry[api_id] = []

    @classmethod
    def register_routers_operation_ids(cls, api: NinjaAPI, router: Router):
        """Register all operation ids registered for a router for an API.

        Args:
            api (NinjaAPI): The API.
            router (Router): The router.

        Raises:
            APINotRegisteredError: If the API is not registered.
            OperationIdOnAPIAlreadyRegisteredError: If the oepration id as already registered for the API.
        """
        api_id = id(api)

        if api_id not in cls.registry:
            raise APINotRegisteredError(api=api)

        operation_ids = RouterOperationRegistry.operation_ids(router=router)

        for operation_id in operation_ids:
            if operation_id in cls.registry[api_id]:
                raise OperationIdOnAPIAlreadyRegisteredError(api=api, operation_id=operation_id)

            cls.registry[api_id].append(operation_id)

    @classmethod
    def operation_ids(cls, api: NinjaAPI) -> list[str]:
        """Get all registered oepration ids registered for a router.

        Args:
            api (NinjaAPI): The APU.

        Raises:
            APINotRegisteredError: If the API is not registered.

        Returns:
            list[str]: The operation ids registered for the API.
        """
        api_id = id(api)

        if api_id not in cls.registry:
            raise APINotRegisteredError(api=api)

        return cls.registry[api_id]
