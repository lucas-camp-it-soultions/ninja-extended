import pytest
from ninja_extended.fields.int import IntField, IntFieldValues
from pydantic_core import PydanticUndefined

DEFAULT_VALUES = [-42, 0, 42, None]


@pytest.fixture
def field_values():
    return IntFieldValues(description="Description")


def test_field_values_default_values(field_values: IntFieldValues):
    assert field_values.description == "Description"
    assert field_values.strict is True
    assert field_values.gt is None
    assert field_values.ge is None
    assert field_values.lt is None
    assert field_values.le is None
    assert field_values.multiple_of is None


def test_field_call_default(field_values: IntFieldValues, mocker):
    field_mock = mocker.patch("ninja_extended.fields.int.BaseField")

    IntField(field_values=field_values)

    field_mock.assert_called_once_with(
        field_values=field_values, default=PydanticUndefined
    )


@pytest.mark.parametrize("default_value", DEFAULT_VALUES)
def test_base_field_call(field_values: IntFieldValues, default_value, mocker):
    field_mock = mocker.patch("ninja_extended.fields.int.BaseField")

    IntField(field_values=field_values, default=default_value)

    field_mock.assert_called_once_with(field_values=field_values, default=default_value)


@pytest.mark.parametrize("default_value", DEFAULT_VALUES)
def test_field_call(field_values: IntFieldValues, default_value, mocker):
    field_mock = mocker.patch("ninja_extended.fields.base.Field")

    IntField(field_values=field_values, default=default_value)

    field_mock.assert_called_once_with(
        **field_values.model_dump(), default=default_value
    )
