import pytest
from api.api import api
from ninja.testing import TestClient

test_client = TestClient(api)


@pytest.fixture
def resource_data():
    return {
        "value_unique": "value",
        "value_unique_together_1": "value",
        "value_unique_together_2": "value",
        "value_not_null": "value",
    }


@pytest.fixture
def resource_data_unique_single():
    return {
        "value_unique": "value",
        "value_unique_together_1": "value1",
        "value_unique_together_2": "value1",
        "value_not_null": "value1",
    }


@pytest.fixture
def resource_data_unique_multiple():
    return {
        "value_unique": "value1",
        "value_unique_together_1": "value",
        "value_unique_together_2": "value",
        "value_not_null": "value1",
    }


@pytest.fixture
def resource_data_not_null():
    return {
        "value_unique": "value",
        "value_unique_together_1": "value",
        "value_unique_together_2": "value",
        "value_not_null": None,
    }


@pytest.fixture
def resource_data_invalid():
    return {
        "value_unique": "a",
        "value_unique_together_1": "value",
        "value_unique_together_2": "value",
        "value_not_null": None,
    }


@pytest.mark.django_db
def test_unique_constraint_single(resource_data, resource_data_unique_single):
    test_client.post(path="/resources", json=resource_data)
    response = test_client.post(path="/resources", json=resource_data_unique_single)

    assert response.status_code == 422
    assert response.data == {
        "type": "errors/resources/unique-constraint",
        "status": 422,
        "title": "Unique constraint violation for Resource.",
        "detail": "Unique constraint violation for Resource with (value_unique='value').",
        "fields": {
            "value_unique": "value",
        },
        "path": "/resources",
        "operation_id": "createResource",
    }


@pytest.mark.django_db
def test_unique_constraint_multiple(resource_data, resource_data_unique_multiple):
    test_client.post(path="/resources", json=resource_data)
    response = test_client.post(path="/resources", json=resource_data_unique_multiple)

    assert response.status_code == 422
    assert response.data == {
        "type": "errors/resources/unique-constraint",
        "status": 422,
        "title": "Unique constraint violation for Resource.",
        "detail": "Unique constraint violation for Resource with (value_unique_together_1='value',value_unique_together_2='value').",
        "fields": {
            "value_unique_together_1": "value",
            "value_unique_together_2": "value",
        },
        "path": "/resources",
        "operation_id": "createResource",
    }


@pytest.mark.django_db
def test_not_null_constraint(resource_data_not_null):
    response = test_client.post(path="/resources", json=resource_data_not_null)

    assert response.status_code == 422
    assert response.data == {
        "type": "errors/resources/not-null-constraint",
        "status": 422,
        "title": "Not null constraint violation for Resource.",
        "detail": "Not null constraint violation for Resource with (value_not_null=null).",
        "fields": {
            "value_not_null": None,
        },
        "path": "/resources",
        "operation_id": "createResource",
    }


@pytest.mark.django_db
def test_validation(resource_data_invalid):
    response = test_client.post(path="/resources", json=resource_data_invalid)

    assert response.status_code == 422
    assert response.data == {
        "type": "errors/create-resource/validation",
        "status": 422,
        "title": "Validation for operation createResource failed.",
        "detail": "Validation for operation createResource failed.",
        "errors": [
            {
                "type": "string_too_short",
                "loc": ["body", "data", "value_unique"],
                "msg": "String should have at least 3 characters",
                "ctx": {
                    "min_length": 3,
                },
            },
        ],
        "path": "/resources",
        "operation_id": "createResource",
    }
