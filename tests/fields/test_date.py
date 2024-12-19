from datetime import date

import pytest
from ninja_extended.fields.date import DateField, DateFieldValues
from pydantic_core import PydanticUndefined

DEFAULT_VALUES = [
    date(year=1970, month=1, day=1),
    None,
]


@pytest.fixture
def field_values():
    return DateFieldValues(description="Description")


def test_field_values_default_values(field_values: DateFieldValues):
    assert field_values.description == "Description"
    assert field_values.strict is True
    assert field_values.gt is None
    assert field_values.ge is None
    assert field_values.lt is None
    assert field_values.le is None


def test_field_call_default(field_values: DateFieldValues, mocker):
    field_mock = mocker.patch("ninja_extended.fields.date.BaseField")

    DateField(field_values=field_values)

    field_mock.assert_called_once_with(
        field_values=field_values, default=PydanticUndefined
    )


@pytest.mark.parametrize("default_value", DEFAULT_VALUES)
def test_base_field_call(field_values: DateFieldValues, default_value, mocker):
    field_mock = mocker.patch("ninja_extended.fields.date.BaseField")

    DateField(field_values=field_values, default=default_value)

    field_mock.assert_called_once_with(field_values=field_values, default=default_value)


@pytest.mark.parametrize("default_value", DEFAULT_VALUES)
def test_field_call(field_values: DateFieldValues, default_value, mocker):
    field_mock = mocker.patch("ninja_extended.fields.base.Field")

    DateField(field_values=field_values, default=default_value)

    field_mock.assert_called_once_with(
        **field_values.model_dump(), default=default_value
    )
