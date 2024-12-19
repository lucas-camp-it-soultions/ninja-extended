import pytest
from ninja_extended.fields.email import EmailField, EmailFieldValues
from pydantic_core import PydanticUndefined

DEFAULT_VALUES = ["foo@bar.com", None]


@pytest.fixture
def field_values():
    return EmailFieldValues(description="Description")


def test_field_values_default_values(field_values: EmailFieldValues):
    assert field_values.description == "Description"


def test_field_call_default(field_values: EmailFieldValues, mocker):
    field_mock = mocker.patch("ninja_extended.fields.email.BaseField")

    EmailField(field_values=field_values)

    field_mock.assert_called_once_with(
        field_values=field_values, default=PydanticUndefined
    )


@pytest.mark.parametrize("default_value", DEFAULT_VALUES)
def test_base_field_call(field_values: EmailFieldValues, default_value, mocker):
    field_mock = mocker.patch("ninja_extended.fields.email.BaseField")

    EmailField(field_values=field_values, default=default_value)

    field_mock.assert_called_once_with(field_values=field_values, default=default_value)


@pytest.mark.parametrize("default_value", DEFAULT_VALUES)
def test_field_call(field_values: EmailFieldValues, default_value, mocker):
    field_mock = mocker.patch("ninja_extended.fields.base.Field")

    EmailField(field_values=field_values, default=default_value)

    field_mock.assert_called_once_with(
        **field_values.model_dump(), default=default_value
    )
