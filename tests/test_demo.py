import pytest
from api.api import api
from api.models import Child1, Child2, Resource
from ninja.testing import TestClient

test_client = TestClient(api)


@pytest.fixture
def resource_data():
    return {
        "value_unique": "value",
        "value_unique_together_1": "value",
        "value_unique_together_2": "value",
        "value_not_null": "value",
        "value_check": 1,
    }


@pytest.fixture
def resource_data_unique_single():
    return {
        "value_unique": "value",
        "value_unique_together_1": "value1",
        "value_unique_together_2": "value1",
        "value_not_null": "value1",
        "value_check": 1,
    }


@pytest.fixture
def resource_data_unique_multiple():
    return {
        "value_unique": "value1",
        "value_unique_together_1": "value",
        "value_unique_together_2": "value",
        "value_not_null": "value1",
        "value_check": 1,
    }


@pytest.fixture
def resource_data_not_null():
    return {
        "value_unique": "value",
        "value_unique_together_1": "value",
        "value_unique_together_2": "value",
        "value_not_null": None,
        "value_check": 1,
    }


@pytest.fixture
def resource_data_check():
    return {
        "value_unique": "value",
        "value_unique_together_1": "value",
        "value_unique_together_2": "value",
        "value_not_null": "value",
        "value_check": -1,
    }


@pytest.fixture
def resource_data_invalid():
    return {
        "value_unique": "a",
        "value_unique_together_1": "value",
        "value_unique_together_2": "value",
        "value_not_null": None,
        "value_check": 1,
    }


@pytest.mark.django_db
def test_unique_constraint_single(resource_data, resource_data_unique_single):
    test_client.post(path="/resources/", json=resource_data)
    response = test_client.post(path="/resources/", json=resource_data_unique_single)

    assert response.status_code == 422
    assert response.data == {
        "type": "errors/unique-constraint",
        "status": 422,
        "resource": "Resource",
        "fields": {
            "value_unique": "value",
        },
        "path": "/resources/",
        "operation_id": "createResource",
    }


@pytest.mark.django_db
def test_unique_constraint_multiple(resource_data, resource_data_unique_multiple):
    test_client.post(path="/resources/", json=resource_data)
    response = test_client.post(path="/resources/", json=resource_data_unique_multiple)

    assert response.status_code == 422
    assert response.data == {
        "type": "errors/unique-constraint",
        "status": 422,
        "resource": "Resource",
        "fields": {
            "value_unique_together_1": "value",
            "value_unique_together_2": "value",
        },
        "path": "/resources/",
        "operation_id": "createResource",
    }


@pytest.mark.django_db
def test_not_null_constraint(resource_data_not_null):
    response = test_client.post(path="/resources/", json=resource_data_not_null)

    assert response.status_code == 422
    assert response.data == {
        "type": "errors/not-null-constraint",
        "status": 422,
        "resource": "Resource",
        "fields": {
            "value_not_null": None,
        },
        "path": "/resources/",
        "operation_id": "createResource",
    }


@pytest.mark.django_db
def test_check_constraint(resource_data_check):
    response = test_client.post(path="/resources/", json=resource_data_check)

    assert response.status_code == 422
    assert response.data == {
        "type": "errors/check-constraint",
        "status": 422,
        "resource": "Resource",
        "path": "/resources/",
        "operation_id": "createResource",
    }


@pytest.mark.django_db
def test_validation(resource_data_invalid):
    response = test_client.post(path="/resources/", json=resource_data_invalid)

    assert response.status_code == 422
    assert response.data == {
        "type": "errors/validation",
        "status": 422,
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
        "path": "/resources/",
        "operation_id": "createResource",
    }


@pytest.mark.django_db
def test_protection(resource_data):
    resource = Resource.objects.create(**resource_data)
    child_1 = Child1.objects.create(resource_id=resource.id)
    child_2 = Child2.objects.create(resource_id=resource.id)
    child_3 = Child2.objects.create(resource_id=resource.id)

    response = test_client.delete(path=f"/resources/{resource.id}")

    assert response.status_code == 422
    assert response.data == {
        "type": "errors/protection",
        "status": 422,
        "resource": "Resource",
        "foreign_items": {
            "Child1": [child_1.id],
            "Child2": [child_2.id, child_3.id],
        },
        "path": "/resources/1",
        "operation_id": "deleteResourceById",
    }


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_pagination():
    for i in range(10):
        value = f"value_{i}"
        Resource.objects.create(
            value_unique=value,
            value_unique_together_1=value,
            value_unique_together_2=value,
            value_not_null=value,
            value_check=1,
        )

    response = test_client.get(path="/resources/pagination")

    assert response.status_code == 200
    assert response.data == {
        "count": 10,
        "pages": 1,
        "current_page": 1,
        "previous_page": None,
        "next_page": None,
        "previous_url": None,
        "next_url": None,
        "items": [
            {
                "id": i + 1,
                "value_unique": f"value_{i}",
                "value_unique_together_1": f"value_{i}",
                "value_unique_together_2": f"value_{i}",
                "value_not_null": f"value_{i}",
                "value_check": 1,
            }
            for i in range(10)
        ],
    }

    # Pagesize 3; Page 1
    response = test_client.get(path="/resources/pagination?page_size=3&page=1")

    assert response.status_code == 200
    assert response.data == {
        "count": 10,
        "pages": 4,
        "current_page": 1,
        "previous_page": None,
        "next_page": 2,
        "previous_url": None,
        "next_url": "http://testlocation/resources/pagination?page_size=3&page=2",
        "items": [
            {
                "id": i + 1,
                "value_unique": f"value_{i}",
                "value_unique_together_1": f"value_{i}",
                "value_unique_together_2": f"value_{i}",
                "value_not_null": f"value_{i}",
                "value_check": 1,
            }
            for i in range(3)
        ],
    }

    # Pagesize 3; Page 2
    response = test_client.get(path="/resources/pagination?page_size=3&page=2")

    assert response.status_code == 200
    assert response.data == {
        "count": 10,
        "pages": 4,
        "current_page": 2,
        "previous_page": 1,
        "next_page": 3,
        "previous_url": "http://testlocation/resources/pagination?page_size=3&page=1",
        "next_url": "http://testlocation/resources/pagination?page_size=3&page=3",
        "items": [
            {
                "id": i + 1,
                "value_unique": f"value_{i}",
                "value_unique_together_1": f"value_{i}",
                "value_unique_together_2": f"value_{i}",
                "value_not_null": f"value_{i}",
                "value_check": 1,
            }
            for i in range(3, 6)
        ],
    }

    # Pagesize 3; Page 3
    response = test_client.get(path="/resources/pagination?page_size=3&page=3")

    assert response.status_code == 200
    assert response.data == {
        "count": 10,
        "pages": 4,
        "current_page": 3,
        "previous_page": 2,
        "next_page": 4,
        "previous_url": "http://testlocation/resources/pagination?page_size=3&page=2",
        "next_url": "http://testlocation/resources/pagination?page_size=3&page=4",
        "items": [
            {
                "id": i + 1,
                "value_unique": f"value_{i}",
                "value_unique_together_1": f"value_{i}",
                "value_unique_together_2": f"value_{i}",
                "value_not_null": f"value_{i}",
                "value_check": 1,
            }
            for i in range(6, 9)
        ],
    }

    # Pagesize 3; Page 4
    response = test_client.get(path="/resources/pagination?page_size=3&page=4")

    assert response.status_code == 200
    assert response.data == {
        "count": 10,
        "pages": 4,
        "current_page": 4,
        "previous_page": 3,
        "next_page": None,
        "previous_url": "http://testlocation/resources/pagination?page_size=3&page=3",
        "next_url": None,
        "items": [
            {
                "id": i + 1,
                "value_unique": f"value_{i}",
                "value_unique_together_1": f"value_{i}",
                "value_unique_together_2": f"value_{i}",
                "value_not_null": f"value_{i}",
                "value_check": 1,
            }
            for i in range(9, 10)
        ],
    }

    # Pagesize 3; Page 5
    response = test_client.get(path="/resources/pagination?page_size=3&page=5")

    assert response.status_code == 422
    assert response.data == {
        "type": "errors/validation",
        "status": 422,
        "errors": [
            {
                "type": "less_than_equal",
                "loc": ["query", "page"],
                "msg": "Input should be less than or equal to 4",
                "ctx": {"le": 4},
            },
        ],
        "path": "/resources/pagination?page_size=3&page=5",
        "operation_id": "listResourcesPagination",
    }
