from typing import Literal, _AnnotatedAlias

from ninja import Schema

from ninja_extended.api import response_factory
from ninja_extended.errors import AuthenticationError, AuthorizationError, CSRFError


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
    response_dict = response_factory((401, AuthenticationError))

    assert isinstance(response_dict, dict)

    assert response_dict == {401: AuthenticationError.schema}


def test_response_factory_multiple_errors_different_status():
    response_dict = response_factory((401, AuthenticationError), (403, AuthorizationError))

    assert isinstance(response_dict, dict)

    assert response_dict == {401: AuthenticationError.schema, 403: AuthorizationError.schema}


def test_response_factory_multiple_errors_same_status():
    response_dict = response_factory((403, AuthorizationError), (403, CSRFError))

    assert isinstance(response_dict, dict)
    assert len(response_dict) == 1

    assert isinstance(response_dict[403], _AnnotatedAlias)
    assert len(response_dict[403].__args__) == 1
    assert len(response_dict[403].__args__[0].__args__) == 2
    assert response_dict[403].__args__[0].__args__ == (AuthorizationError.schema, CSRFError.schema)


def test_response_factory_single_schema_multiple_errors():
    response_dict = response_factory(
        (200, SchemaA), (401, AuthenticationError), (403, AuthorizationError), (403, CSRFError)
    )

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
    response_dict = response_factory(
        (200, list[SchemaA]), (401, AuthenticationError), (403, AuthorizationError), (403, CSRFError)
    )

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
