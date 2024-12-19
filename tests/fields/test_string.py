import pytest
from ninja_extended.fields.string import StringField, StringFieldValues
from pydantic_core import PydanticUndefined

DEFAULT_VALUES = [True, False, None]


@pytest.fixture
def field_values():
    return StringFieldValues(description="Description")


def test_field_values_default_values(field_values: StringFieldValues):
    assert field_values.description == "Description"
    assert field_values.strict is True
    assert field_values.strip_whitespace is None
    assert field_values.to_upper is None
    assert field_values.to_lower is None
    assert field_values.min_length is None
    assert field_values.max_length is None
    assert field_values.pattern is None


def test_field_call_default(field_values: StringFieldValues, mocker):
    field_mock = mocker.patch("ninja_extended.fields.string.BaseField")

    StringField(field_values=field_values)

    field_mock.assert_called_once_with(
        field_values=field_values, default=PydanticUndefined
    )


@pytest.mark.parametrize("default_value", DEFAULT_VALUES)
def test_base_field_call(field_values: StringFieldValues, default_value, mocker):
    field_mock = mocker.patch("ninja_extended.fields.string.BaseField")

    StringField(field_values=field_values, default=default_value)

    field_mock.assert_called_once_with(field_values=field_values, default=default_value)


@pytest.mark.parametrize("default_value", DEFAULT_VALUES)
def test_field_call(field_values: StringFieldValues, default_value, mocker):
    field_mock = mocker.patch("ninja_extended.fields.base.Field")

    StringField(field_values=field_values, default=default_value)

    field_mock.assert_called_once_with(
        **field_values.model_dump(), default=default_value
    )
