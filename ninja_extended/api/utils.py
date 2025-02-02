"""Module api.utils."""

from inspect import (
    _KEYWORD_ONLY,
    _POSITIONAL_ONLY,
    _POSITIONAL_OR_KEYWORD,
    _VAR_KEYWORD,
    _VAR_POSITIONAL,
    FullArgSpec,
    Signature,
    _signature_from_callable,
)
from types import GenericAlias
from typing import Annotated, _AnnotatedAlias

from ninja import Schema
from pydantic import Field

from ninja_extended.api.api import ExtendedNinjaAPI
from ninja_extended.api.errors import OperationIdNotFoundInAPIError, OperationIdNotFoundInRouterError
from ninja_extended.api.operation import ExtendedOperation
from ninja_extended.api.router import ExtendedRouter
from ninja_extended.errors import APIError


def response_factory(*responses: tuple[int, type[Schema]] | type[APIError]):
    """Create a response dictionary from a list of responses.

    Args:
        *responses (tuple[int, type[Schema] | type[APIError]]): The responses.

    Returns:
        dict[int, type[Schema]]: A dictionary of responses.
    """

    invalid_response_message = (
        "Invalid response provided. Must be tuple[int, type[Schema] | type[_AnnotatedAlias]] or type[APIError]."
    )
    invalid_response_tuple_message = "Invalid response tuple provided. Must be tuple[int, type[Schema]]."
    response_dict = {}

    for response in responses:
        if isinstance(response, tuple):
            if len(response) != 2:  # noqa: PLR2004
                raise TypeError(invalid_response_tuple_message)

            status_code, response_schema = response

            if not isinstance(status_code, int):
                raise TypeError(invalid_response_tuple_message)

            if (
                response_schema is not None
                and not (
                    isinstance(response_schema, type | GenericAlias)
                    and hasattr(response_schema, "__origin__")
                    and response_schema.__origin__ is list
                )
                and not issubclass(response_schema, Schema)
            ):
                raise TypeError(invalid_response_tuple_message)
        elif issubclass(response, APIError):
            status_code = response.status
            response_schema = response.schema
        else:
            raise TypeError(invalid_response_message)

        if status_code in response_dict:
            existing_schema = response_dict[status_code]
            combined_schema = Annotated[existing_schema | response_schema, Field(discriminator="type")]
            response_dict[status_code] = combined_schema
        else:
            response_dict[status_code] = response_schema

    return response_dict


def get_operation_from_api_by_operation_id(api: ExtendedNinjaAPI, operation_id: str) -> ExtendedOperation:
    """Get an operation from an api by its operation id.

    Args:
        api (ExtendedNinjaAPI): The api.
        operation_id (str): The operation id.

    Raises:
        OperationIdNotFoundError: If the operation id is not found.

    Returns:
        ExtendedOperation: The operation.
    """

    for _, router in api._routers:  # noqa: SLF001
        for path_operation in router.path_operations.values():
            for operation in path_operation.operations:
                if operation.operation_id == operation_id:
                    return operation

    raise OperationIdNotFoundInAPIError(api=api, operation_id=operation_id)


def get_operation_from_router_by_operation_id(router: ExtendedRouter, operation_id: str) -> ExtendedOperation:
    """Get an operation from a router by its operation id.

    Args:
        router (ExtendedRouter): The router.
        operation_id (str): The operation id.

    Raises:
        OperationIdNotFoundError: If the operation id is not found.

    Returns:
        ExtendedOperation: The operation.
    """
    for path_operation in router.path_operations.values():
        for operation in path_operation.operations:
            if operation.operation_id == operation_id:
                return operation

    raise OperationIdNotFoundInRouterError(router=router, operation_id=operation_id)


def is_response_registered_in_operation(  # noqa: PLR0912
    api_or_router: ExtendedNinjaAPI | ExtendedRouter,
    operation_id: str,
    response: tuple[int, type[Schema]] | type[APIError],
):
    """Check if a response schema is registered in the operation with given operation id.

    Args:
        api_or_router (ExtendedNinjaAPI | ExtendedRouter): The api or router.
        operation_id (str): The operation_id
        response (tuple[int, type[Schema]] | type[APIError]): The response.

    Raises:
        TypeError: If the response has an invalid type.

    Returns:
        bool: If the response schema is registered.
    """

    invalid_app_or_router_type_message = "Invalid app or router provided. Must be ExtendedNinjaAPI | ExtendedRouter."
    invalid_response_message = "Invalid response provided. Must be tuple[int, type[Schema]] or type[APIError]."
    invalid_response_tuple_message = "Invalid response tuple provided. Must be tuple[int, type[Schema]]."

    if isinstance(response, tuple):
        if len(response) != 2:  # noqa: PLR2004
            raise TypeError(invalid_response_tuple_message)

        status, response_schema = response

        if not isinstance(status, int):
            raise TypeError(invalid_response_tuple_message)

        if (
            response_schema is not None
            and not (
                isinstance(response_schema, type | GenericAlias)
                and hasattr(response_schema, "__origin__")
                and response_schema.__origin__ is list
            )
            and not issubclass(response_schema, Schema)
        ):
            raise TypeError(invalid_response_tuple_message)
    elif issubclass(response, APIError):
        status = response.status
        response_schema = response.schema
    else:
        raise TypeError(invalid_response_message)

    if isinstance(api_or_router, ExtendedNinjaAPI):
        operation = get_operation_from_api_by_operation_id(api=api_or_router, operation_id=operation_id)
    elif isinstance(api_or_router, ExtendedRouter):
        operation = get_operation_from_router_by_operation_id(router=api_or_router, operation_id=operation_id)
    else:
        raise TypeError(invalid_app_or_router_type_message)

    for status_code, response_ in operation.response.items():
        if isinstance(response_, _AnnotatedAlias) and len(response_.__args__) == 1:
            if response_schema in response_.__args__[0].__args__:
                return True
        elif status == status_code and response_ == response_schema:
            return True

    return False


def get_full_arg_spec(func):  # noqa: PLR0912
    """Get the full argument specification for the given callable."""

    try:
        sig = _signature_from_callable(
            func, follow_wrapper_chains=True, skip_bound_arg=False, sigcls=Signature, eval_str=False
        )
    except Exception as ex:
        # Most of the times 'signature' will raise ValueError.
        # But, it can also raise AttributeError, and, maybe something
        # else. So to be fully backwards compatible, we catch all
        # possible exceptions here, and reraise a TypeError.
        raise TypeError("unsupported callable") from ex  # noqa: EM101

    args = []
    varargs = None
    varkw = None
    posonlyargs = []
    kwonlyargs = []
    annotations = {}
    defaults = ()
    kwdefaults = {}

    if sig.return_annotation is not sig.empty:
        annotations["return"] = sig.return_annotation

    for param in sig.parameters.values():
        kind = param.kind
        name = param.name

        if kind is _POSITIONAL_ONLY:
            posonlyargs.append(name)
            if param.default is not param.empty:
                defaults += (param.default,)
        elif kind is _POSITIONAL_OR_KEYWORD:
            args.append(name)
            if param.default is not param.empty:
                defaults += (param.default,)
        elif kind is _VAR_POSITIONAL:
            varargs = name
        elif kind is _KEYWORD_ONLY:
            kwonlyargs.append(name)
            if param.default is not param.empty:
                kwdefaults[name] = param.default
        elif kind is _VAR_KEYWORD:
            varkw = name

        if param.annotation is not param.empty:
            annotations[name] = param.annotation

    if not kwdefaults:
        # compatibility with 'func.__kwdefaults__'
        kwdefaults = None

    if not defaults:
        # compatibility with 'func.__defaults__'
        defaults = None

    return FullArgSpec(posonlyargs + args, varargs, varkw, defaults, kwonlyargs, kwdefaults, annotations)
