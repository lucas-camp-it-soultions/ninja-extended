from datetime import datetime, timedelta

import pytest
from pydantic_core import PydanticUndefined

from ninja_extended.fields.datetime import DatetimeField, DatetimeFieldValues

DEFAULT_VALUES = [
    datetime.now() - timedelta(seconds=1),
    datetime.now(),
    datetime.now() + timedelta(seconds=1),
    None,
]


@pytest.fixture
def field_values():
    return DatetimeFieldValues(description="Description")


def test_field_values_default_values(field_values: DatetimeFieldValues):
    assert field_values.description == "Description"
    assert field_values.strict is True
    assert field_values.gt is None
    assert field_values.ge is None
    assert field_values.lt is None
    assert field_values.le is None


def test_field_call_default(field_values: DatetimeFieldValues, mocker):
    field_mock = mocker.patch("ninja_extended.fields.datetime.BaseField")

    DatetimeField(field_values=field_values)

    field_mock.assert_called_once_with(field_values=field_values, default=PydanticUndefined)


@pytest.mark.parametrize("default_value", DEFAULT_VALUES)
def test_base_field_call(field_values: DatetimeFieldValues, default_value, mocker):
    field_mock = mocker.patch("ninja_extended.fields.datetime.BaseField")

    DatetimeField(field_values=field_values, default=default_value)

    field_mock.assert_called_once_with(field_values=field_values, default=default_value)


@pytest.mark.parametrize("default_value", DEFAULT_VALUES)
def test_field_call(field_values: DatetimeFieldValues, default_value, mocker):
    field_mock = mocker.patch("ninja_extended.fields.base.Field")

    DatetimeField(field_values=field_values, default=default_value)

    field_mock.assert_called_once_with(**field_values.model_dump(), default=default_value)
