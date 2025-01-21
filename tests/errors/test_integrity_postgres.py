import pytest
from api.models import Resource
from django.db import IntegrityError

from ninja_extended.errors.integrity import (
    IntegrityErrorParser,
    PostgresIntegrityErrorParser,
    PostgresNotNullIntegrityErrorParser,
    PostgresUniqueConstraintIntegrityErrorParser,
)
from ninja_extended.errors.integrity.types import IntegrityErrorType


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
def resource_data_check():
    return {
        "value_unique": "value",
        "value_unique_together_1": "value",
        "value_unique_together_2": "value",
        "value_not_null": "value",
        "value_check": -1,
    }


@pytest.fixture
def resource_data_not_null():
    return {
        "value_unique": "value",
        "value_unique_together_1": "value",
        "value_unique_together_2": "value",
        "value_not_null": None,
    }


@pytest.mark.django_db(databases=["postgres"])
def test_unique_constraint_single_postgres_unique_constraint(resource_data, resource_data_unique_single):
    Resource.objects.using("postgres").create(**resource_data)

    with pytest.raises(IntegrityError) as error:
        Resource.objects.using("postgres").create(**resource_data_unique_single)
    assert PostgresUniqueConstraintIntegrityErrorParser().parse(error=error.value) == (
        IntegrityErrorType.UNIQUE_CONSTRAINT,
        ["value_unique"],
    )


@pytest.mark.django_db(databases=["postgres"])
def test_unique_constraint_single_postgres(resource_data, resource_data_unique_single):
    Resource.objects.using("postgres").create(**resource_data)

    with pytest.raises(IntegrityError) as error:
        Resource.objects.using("postgres").create(**resource_data_unique_single)
    assert PostgresIntegrityErrorParser().parse(error=error.value) == (
        IntegrityErrorType.UNIQUE_CONSTRAINT,
        ["value_unique"],
    )


@pytest.mark.django_db(databases=["postgres"])
def test_unique_constraint_single(resource_data, resource_data_unique_single):
    Resource.objects.using("postgres").create(**resource_data)

    with pytest.raises(IntegrityError) as error:
        Resource.objects.using("postgres").create(**resource_data_unique_single)
    assert IntegrityErrorParser().parse(error=error.value) == (IntegrityErrorType.UNIQUE_CONSTRAINT, ["value_unique"])


@pytest.mark.django_db(databases=["postgres"])
def test_unique_constraint_multiple_postgres_unique_constraint(resource_data, resource_data_unique_multiple):
    Resource.objects.using("postgres").create(**resource_data)

    with pytest.raises(IntegrityError) as error:
        Resource.objects.using("postgres").create(**resource_data_unique_multiple)
    assert PostgresUniqueConstraintIntegrityErrorParser().parse(error=error.value) == (
        IntegrityErrorType.UNIQUE_CONSTRAINT,
        ["value_unique_together_1", "value_unique_together_2"],
    )


@pytest.mark.django_db(databases=["postgres"])
def test_unique_constraint_multiple_postgres(resource_data, resource_data_unique_multiple):
    Resource.objects.using("postgres").create(**resource_data)

    with pytest.raises(IntegrityError) as error:
        Resource.objects.using("postgres").create(**resource_data_unique_multiple)
    assert PostgresIntegrityErrorParser().parse(error=error.value) == (
        IntegrityErrorType.UNIQUE_CONSTRAINT,
        ["value_unique_together_1", "value_unique_together_2"],
    )


@pytest.mark.django_db(databases=["postgres"])
def test_unique_constraint_multiple(resource_data, resource_data_unique_multiple):
    Resource.objects.using("postgres").create(**resource_data)

    with pytest.raises(IntegrityError) as error:
        Resource.objects.using("postgres").create(**resource_data_unique_multiple)
    assert IntegrityErrorParser().parse(error=error.value) == (
        IntegrityErrorType.UNIQUE_CONSTRAINT,
        ["value_unique_together_1", "value_unique_together_2"],
    )


@pytest.mark.django_db(databases=["postgres"])
def test_not_null_constraint_postgres_not_null_constraint(resource_data_not_null):
    with pytest.raises(IntegrityError) as error:
        Resource.objects.using("postgres").create(**resource_data_not_null)
    assert PostgresNotNullIntegrityErrorParser().parse(error=error.value) == (
        IntegrityErrorType.NOT_NULL_CONSTRAINT,
        ["value_not_null"],
    )


@pytest.mark.django_db(databases=["postgres"])
def test_not_null_constraint_postgres(resource_data_not_null):
    with pytest.raises(IntegrityError) as error:
        Resource.objects.using("postgres").create(**resource_data_not_null)
    assert PostgresIntegrityErrorParser().parse(error=error.value) == (
        IntegrityErrorType.NOT_NULL_CONSTRAINT,
        ["value_not_null"],
    )


@pytest.mark.django_db(databases=["postgres"])
def test_not_null_constraint(resource_data_not_null):
    with pytest.raises(IntegrityError) as error:
        Resource.objects.using("postgres").create(**resource_data_not_null)
    assert IntegrityErrorParser().parse(error=error.value) == (
        IntegrityErrorType.NOT_NULL_CONSTRAINT,
        ["value_not_null"],
    )


@pytest.mark.django_db(databases=["postgres"])
def test_check_constraint(resource_data_check):
    with pytest.raises(IntegrityError) as error:
        Resource.objects.using("postgres").create(**resource_data_check)
    assert IntegrityErrorParser().parse(error=error.value) == (
        IntegrityErrorType.CHECK_CONSTRAINT,
        ["value_check_gte_0"],
    )
