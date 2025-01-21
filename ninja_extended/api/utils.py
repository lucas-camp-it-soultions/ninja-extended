"""Module api.utils."""

from typing import Annotated

from ninja import Schema
from pydantic import Field

from ninja_extended.errors import APIError


def response_factory(*responses: tuple[int, type[Schema] | type[APIError]]):
    """Create a response dictionary from a list of responses.

    Args:
        *responses (tuple[int, type[Schema] | type[APIError]]): The responses.

    Returns:
        dict[int, type[Schema]]: A dictionary of responses.
    """

    response_dict = {}

    for status_code, response_type in responses:
        if (
            isinstance(response_type, type)
            and hasattr(response_type, "__origin__")
            and response_type.__origin__ is list
        ):
            response_schema = response_type
        elif issubclass(response_type, APIError):
            response_schema = response_type.schema
        else:
            response_schema = response_type

        if status_code in response_dict:
            existing_schema = response_dict[status_code]
            combined_schema = Annotated[existing_schema | response_schema, Field(discriminator="type")]
            response_dict[status_code] = combined_schema
        else:
            response_dict[status_code] = response_schema

    return response_dict
