"""Definition of error classes for Djangi Ninja Extnded API."""

from ninja import NinjaAPI, Router


class APIConfigurationError(Exception):
    """Base error for an invalid API configuration."""

    def __init__(self, message: str):
        """Initialize an APIConfigurationError.

        Args:
            message (str): The message.
        """

        super().__init__(message)


class HttpMethodOnAPINotAllowedError(APIConfigurationError):
    """Error for an unallowed HTTP method."""

    def __init__(self, method: str):
        """HttpMethodOnAPINotAllowedError.

        Args:
            method (str): The HTTP method.
        """

        super().__init__(f"HTTP method '{method}' on ExtendedNinjaAPI instance not allowed.")


class RouterAlreadyRegisteredError(APIConfigurationError):
    """Error for an already registered router."""

    def __init__(self, router: Router):
        """Initialize a RouterAlreadyRegisteredError.

        Args:
            router (Router): The router.
        """

        super().__init__(f"Router with id {id(router)} already registered.")


class RouterNotRegisteredError(APIConfigurationError):
    """Error for a not registered router."""

    def __init__(self, router: Router):
        """Initialize a RouterNotRegisteredError.

        Args:
            router (Router): The router.
        """

        super().__init__(f"Router with id {id(router)} is not registered.")


class APIAlreadyRegisteredError(APIConfigurationError):
    """Error for an already registered API."""

    def __init__(self, api: NinjaAPI):
        """Initialize an APIAlreadyRegisteredError.

        Args:
            api (NinjaAPI): The API.
        """
        super().__init__(f"API with id {id(api)} already registered.")


class APINotRegisteredError(APIConfigurationError):
    """Error for a not registered API."""

    def __init__(self, api: NinjaAPI):
        """Initialize an APINotRegisteredError.

        Args:
            api (NinjaAPI): The API.
        """
        super().__init__(f"API with id {id(api)} is not registered.")


class OperationIdOnRouterAlreadyRegisteredError(APIConfigurationError):
    """Error for an already registered operation id for a router."""

    def __init__(self, router: Router, operation_id: str):
        """Initialize an OperationIdOnRouterAlreadyRegisteredError.

        Args:
            router (Router): The router.
            operation_id (str): The operation id.
        """
        super().__init__(f"Operation id '{operation_id}' already registered on router with id {id(router)}.")


class OperationIdOnAPIAlreadyRegisteredError(APIConfigurationError):
    """Error for an already registered operation id for an API."""

    def __init__(self, api: NinjaAPI, operation_id: str):
        """Initialize an OperationIdOnAPIAlreadyRegisteredError.

        Args:
            api (NinjaAPI): The API.
            operation_id (str): The operation id.
        """
        super().__init__(f"Operation id '{operation_id}' already registered on api with id {id(api)}.")


class OperationIdNotFoundInAPIError(APIConfigurationError):
    """Error for a not found operation id in an api."""

    def __init__(self, api: NinjaAPI, operation_id: str):
        """Initialize an OperationIdNotFoundError.

        Args:
            api (NinjaAPI): The api.
            operation_id (str): The operation id.
        """
        super().__init__(f"Operation id '{operation_id}' not found in api with id {id(api)}.")


class OperationIdNotFoundInRouterError(APIConfigurationError):
    """Error for a not found operation id in a router."""

    def __init__(self, router: Router, operation_id: str):
        """Initialize an OperationIdNotFoundError.

        Args:
            router (Router): The router.
            operation_id (str): The operation id.
        """
        super().__init__(f"Operation id '{operation_id}' not found in router with id {id(router)}.")
