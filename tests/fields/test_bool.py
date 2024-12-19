import pytest
from ninja_extended.fields.bool import BoolField, BoolFieldValues
from pydantic_core import PydanticUndefined

DEFAULT_VALUES = [True, False, None]


@pytest.fixture
def field_values():
    return BoolFieldValues(description="Description")


def test_field_values_default_values(field_values: BoolFieldValues):
    assert field_values.description == "Description"


def test_field_call_default(field_values: BoolFieldValues, mocker):
    field_mock = mocker.patch("ninja_extended.fields.bool.BaseField")

    BoolField(field_values=field_values)

    field_mock.assert_called_once_with(
        field_values=field_values, default=PydanticUndefined
    )


@pytest.mark.parametrize("default_value", DEFAULT_VALUES)
def test_base_field_call(field_values: BoolFieldValues, default_value, mocker):
    field_mock = mocker.patch("ninja_extended.fields.bool.BaseField")

    BoolField(field_values=field_values, default=default_value)

    field_mock.assert_called_once_with(field_values=field_values, default=default_value)


@pytest.mark.parametrize("default_value", DEFAULT_VALUES)
def test_field_call(field_values: BoolFieldValues, default_value, mocker):
    field_mock = mocker.patch("ninja_extended.fields.base.Field")

    BoolField(field_values=field_values, default=default_value)

    field_mock.assert_called_once_with(
        **field_values.model_dump(), default=default_value
    )
